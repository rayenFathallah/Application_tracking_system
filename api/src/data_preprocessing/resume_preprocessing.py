from deep_translator import GoogleTranslator
from langdetect import detect
import nltk
import re
import pandas as pd
from src.exception import CustomException
from src.logger import logging
import spacy
from spacy.matcher import PhraseMatcher
from fuzzywuzzy import fuzz
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from numpy.linalg import norm
def remove_initial_newlines(text):
    sentence_found = False
    new_text = ''

    for char in text:
        if not sentence_found:
            if char == '\n':
                continue
            else:
                sentence_found = True
                new_text += char
        else:
            new_text += char

    return new_text
def remove_first_lines(text):
    first_lines_removed= remove_initial_newlines(text)
    return '\n'.join(first_lines_removed.split('\n', 1)[1:])
def detect_lang(resume_text) :
    try :
        lang = detect(resume_text)
        if lang == 'fr' :
            final_text=list()
            for i in range(0, len(resume_text), 50000):
                translation = GoogleTranslator(source='auto', target='en').translate(resume_text[i:i+50000], dest='en')
                final_text.append(translation)
            return ' '.join(final_text) 
        else : 
            return resume_text
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while detecting the language: " + str(e))
        return resume_text
def extract_number(text)  :
    regex_formats = [
        r'\d{8}',
        r'\+216\d{8}',
        r'\d{2}\s?\d{3}\s?\d{3}',
        r'\+216\s?\d{2}\s?\d{3}\s?\d{3}'
    ]
    phone_numbers = set()
    try : 
        for regex_format in regex_formats:
            matches = re.findall(regex_format, text)
            phone_numbers.update(matches)

        return list(phone_numbers)
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the phone number: " + str(e))
        return phone_numbers
def extract_email(resume_text) :
    try :
      email_addresses = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+",resume_text )
      email_address = str()
      # Clean the email addresses using NLTK
      email_addresses = [nltk.word_tokenize(email) for email in email_addresses]

      # Print the email addresses
      if len(email_addresses)>0 :
        email_address ="".join(email_addresses[0])
      
      return email_address
    
    except Exception as e:
      # Catch any other exceptions and log error message
      logging.error("Error while Extracting the email: " + str(e))
      return ''
def find_closest_faculty(input_text, faculty_list):
  '''If the name of the faculty is falsely written, this functions detects it and returns the closest detected name '''
  closest_similarity = 0
  closest_faculty = None

  for faculty in faculty_list:
      similarity = fuzz.partial_ratio(input_text, faculty)
      if similarity > closest_similarity:
          closest_similarity = similarity
          closest_faculty = faculty

  return closest_faculty
def extract_education(text):
    facultes = pd.read_csv('data/data_facs/abbrev_names.csv')
    list_facultes = [remove_accents(elem.lower()) for elem in facultes['Ecole'].to_list()]
    keywords = ['ecole ', 'institut ', 'faculté ', 'lycee ', 'école ','faculty ','institute ',] + list_facultes
    niveau = ['licence ', 'cycle ingenieur ', 'ingenieurie en ', 'master ', 'mastère ','phd','doctorat ','engineering ','engineer ','bachelor ','B.E ', 'post-graduate ','pre-engineering ','preparatoire ','prepa']
    programs = ['licence ','cycle ingenieure' 'cycle ingenieur ', 'ingenieurie en ', 'master ', 'mastère ', 'diplôme ','phd','diplome','doctorat ','engineering ','engineer ','bachelor ','B.E ', 'post-graduate ','pre-engineering ','preparatoire ','prepa']
    exact_institut=set()
    institute_names=set()
    programmes =set()
    matching_niveau=set()
    try : 
        text = text.lower()  # Convert the whole text to lowercase
        exact_names = pd.read_csv('data/data_facs/full_exact_names.csv',sep=';')

        exact_names_list = [remove_accents(elem.lower()) for elem in exact_names['nom'].to_list()]+list_facultes
        for institute in exact_names_list:
            if institute.lower() == "esprit":
                pattern = rf"\b(?!d' |de ){re.escape(institute)}(?:[\d.]*)\b"
            else : 
                pattern = rf"\b{re.escape(institute)}(?:[\d.]*)\b"
            match = re.search(pattern, text.replace('\n',' '))
            if match:
                exact_institut.add(match.group())

        # Modify the institute_pattern to use word boundaries and case-insensitive matching
        institute_pattern = r'\b({})\b(.*?)\n\n'.format('|'.join(keywords), re.IGNORECASE)
        # Modify the program_pattern to use word boundaries and case-insensitive matching
        program_pattern = r'\b({})\b(.*?)\n\n'.format('|'.join(programs), re.IGNORECASE)

        institute_matches = re.findall(institute_pattern, text, re.DOTALL)
        program_matches = re.findall(program_pattern, text, re.DOTALL)

        institute_names = set(['{}{}'.format(match[0].replace('\n', ' '), match[1].replace('\n', ' ').strip()) for match in institute_matches]) 

        programmes = set(['{}{}'.format(match[0].replace('\n',' '), match[1].strip().replace('\n',' ')) for match in program_matches])
        pattern_niveau = r'\b(?:' + '|'.join(re.escape(word) for word in niveau) + r')\b'
        # Use the regular expression to find all matching words in the text
        matching_niveau = set(re.findall(pattern_niveau, text, re.IGNORECASE))
        if(len(exact_institut) <1) : 
           exact_institut.add(find_closest_faculty(text,list_facultes))
        return {'programs': list(programmes), 'institut_plus_info': list(institute_names),'exact_institute' : list(exact_institut),'niveau_exacte': detect_niveau_similarity(list(matching_niveau))}
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the education: " + str(e))
        return {'programs': list(programmes), 'institut_plus_info': list(institute_names),'exact_institute' : list(exact_institut),'niveau_exacte': detect_niveau_similarity(list(matching_niveau))}

# init params of skill extractor

def annot_skills(resume_text,skill_extractor) :
   #Extracts skills from resume text, returns annotated text
   # init params of skill extractor
    #nlp = spacy.load("en_core_web_lg")
    # init skill extractor
    #skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    annotation = skill_extractor.annotate(resume_text)
    return annotation
def get_skills(annoted_results) :
  results = []
  for elem in annoted_results['results']['full_matches'] + annoted_results['results']['ngram_scored'] :
      results.append(elem['doc_node_value'])
  return results
def check_constraints(expression):
  unwanted_words = ['com','www','en']
  min_length = lambda word: (len(word) >= 2 or word.lower() == 'c')
  no_com =lambda word: word not in unwanted_words
  no_tunis = lambda word: word != "tunis"
  no_special_characters= lambda word: bool(re.match('^[a-zA-Z0-9]*$', word))
  final_results = set()
  for word in expression:
    if (min_length(word) and no_com(word) and no_tunis(word) and no_special_characters(word)) :
      final_results.add(word)
  return list(final_results)
def extract_skills(resume_text,skill_extractor) : 
    final_skills = []
    resume_text = resume_text.replace(',',' ')
    try : 
        annot = annot_skills(resume_text,skill_extractor)
        skills = get_skills(annot)
        final_skills = check_constraints(skills)
        return final_skills
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the skillls: " + str(e))
        return final_skills
def extract_skills2(resume_text,jd_model): 
    label_list_jd=list()
    text_list_jd = list()
    dic_jd = {}

    doc_jd = jd_model(resume_text)
    for ent in doc_jd.ents:
        label_list_jd.append(ent.label_)
        text_list_jd.append(ent.text)
    for index in range(len(label_list_jd)) : 
        if label_list_jd[index] in dic_jd.keys() : 
            dic_jd[label_list_jd[index]].append(text_list_jd[index])
        else : 
            dic_jd[label_list_jd[index]] = [text_list_jd[index]]
    return dic_jd['SKILLS']

def remove_accents(input_string):
    accents = {'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'à': 'a',
        'â': 'a',
        'ç': 'c',
        'î': 'i',
        'ï': 'i',
        'ô': 'o',
        'ù': 'u',
        'û': 'u'
        # Add more replacements as needed
    }
     # Add more mappings as needed
    
    for accent, replacement in accents.items():
        input_string = input_string.replace(accent, replacement)
    
    return input_string
def extract_years_of_experience(text):
    years_of_experience = 0 
    try : 
        text2=remove_accents(text)
        # Regular expressions to match various formats of years of experience
        patterns = [
            r'(\d+)\s*(?:year|ann[ee]e|ans)\s*(?:of\s*experience|d[\'e]xperience)?',
            r'(\+\d+)\s*(?:year|ans)\s*experience',
            r'with\s*(\d+)\s*\+\s*years\s*(?:of\s*)?experience',
            r'(\d+)\s*(?:year|ans)\s*(?:in|of)?\s*experience'
            r'(\d+)\s*(?:year|ans)\s*(?:in|of)?\s*(?:experience)?\s*(?:in|of)?\s*',
            r'years\s*of\s*experience\s*:\s*(\d+)',
            r'experience\s*:\s*(\d+)',
            r'annees\s*d\'experience\s*:\s*(\d+)',
            r'ans\s*d\'experience\s*:\s*(\d+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, text2, re.IGNORECASE)
            if match:
                years_of_experience = int(match.group(1))
                break
        return years_of_experience
    except Exception as e:
        # Catch any other exceptions and log error message
        logging.error("Error while Extracting the informations: " + str(e))
        return years_of_experience

def extract_all_info(resume_text,model2) : 
    infos = dict()
    infos['text'] = resume_text
    infos['year_of_experience']= 0 
    infos['email'] = '' 
    infos['education'] = {} 
    infos['skills']=[] 
    infos['number']=set()
    try : 
        infos['number'] = extract_number(resume_text) 
        infos['email'] = extract_email(resume_text) 
        infos['education'] = extract_education(resume_text) 
        infos['skills'] = list(set(extract_skills2(resume_text,model2)))
        infos['year_of_experience'] = extract_years_of_experience(resume_text)
        return infos 
    except Exception as e:
        # Catch any other exceptions and log error message
        logging.error("Error while Extracting the informations: " + str(e))
        return infos
def detect_niveau_similarity(niveau) : 
    '''
    Associate level of experience or after high school studies to a degree. 
    I.g : bac +5 => Ingenieurie 
    I.g : minimum bac +3 => licence, master, ingenieurie 
    '''
    # possible associations  : licence, ingenieurie, preparatoire, mastere, doctorat
    assoc_dic ={ 'licence' : 'licence',
                'cycle ingenieur' : 'ingernieurie', 
                'ingenieurie en' : 'ingernieurie',
                'ingernieurie' : 'ingernieurie',
                'engineering' :'ingernieurie', 
                'engineer' : 'ingernieurie', 
                'bachelor' : 'licence', 
                'B.E' : 'licence', 
                'B.S': 'licence',
                'preparatoire' : 'preparatoire', 
                'prepa' : 'prepa',
                'mastere': 'mastere',
                'master' : 'mastere',
                'doctorat' : 'doctorat',
                'phd' : 'doctorat',
                'graduate' : 'mastere',
                'post-graduate' :'mastere',
                'bac +3' : 'licence', 
                'bac +5' : 'ingenieurie',
                'baccalaureat +5' : 'ingenieurie'
    }
    matched_niveau = []
    for elem in niveau :
        elem = elem.strip() 
        if elem in assoc_dic.keys() : 
            matched_niveau.append(assoc_dic[elem]) 
    return matched_niveau 
def cleanResume(resumeText):
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText
def preprocess_resume_text(text):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    text = cleanResume(text)
    ''' 
lemmetizing Example:

Original: jumping, jumps, jumped
Lemmatized: jump
'''
    filtered_text = ' '.join([word for word in word_tokenize(text) if word.lower() not in stop_words and not word.isdigit()])
    tokens = word_tokenize(filtered_text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    #stemmed_tokens = [stemmer.stem(token) for token in lemmatized_tokens]
    
    return ' '.join(lemmatized_tokens)


def resume_preprocessing_model(resume_text) : 
    translated = detect_lang(resume_text) 
# Call the preprocessor function
    processed_resume = preprocess_resume_text(translated)
    return processed_resume


