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
  lang = detect(resume_text)
  if lang == 'fr' :
    translated_text = GoogleTranslator(source='auto', target='en').translate(resume_text)
    return translated_text
  else :
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
    list_facultes = [elem.lower() for elem in facultes['Ecole'].to_list()]
    keywords = ['ecole ', 'institut ', 'faculté ', 'lycée ', 'école ','faculty ','institute ',] + list_facultes
    programs = ['licence ', 'cycle ', 'ingénieurie ', 'master ', 'mastère ', 'diplôme ','phd','doctorat ','engineering ','engineer ','bachelor ','B.E ','graduate ', 'post-graduate ','pre-engineering ','préparatoire ']
    exact_institut=[]
    institute_names=[]
    programmes =[]
    try : 
        text = text.lower()  # Convert the whole text to lowercase
        exact_names = pd.read_csv('data/data_facs/full_exact_names.csv',sep=';')
        exact_names_list = [elem.lower() for elem in exact_names['nom'].to_list()]+list_facultes
        for institute in exact_names_list:
            pattern = r"\b" + institute + r"\b"
            match = re.search(pattern, text.replace('\n',' '))
            if match:
                exact_institut.append(match.group())

        # Modify the institute_pattern to use word boundaries and case-insensitive matching
        institute_pattern = r'\b({})\b(.*?)\n\n'.format('|'.join(keywords), re.IGNORECASE)
        # Modify the program_pattern to use word boundaries and case-insensitive matching
        program_pattern = r'\b({})\b(.*?)\n\n'.format('|'.join(programs), re.IGNORECASE)

        institute_matches = re.findall(institute_pattern, text, re.DOTALL)
        program_matches = re.findall(program_pattern, text, re.DOTALL)

        institute_names = ['{}{}'.format(match[0].replace('\n', ' '), match[1].replace('\n', ' ').strip()) for match in institute_matches]

        programmes = ['{}{}'.format(match[0].replace('\n',' '), match[1].strip().replace('\n',' ')) for match in program_matches]
        if(len(exact_institut) <1) : 
           exact_institut.append(find_closest_faculty(text,list_facultes))
        return {'programs': programmes, 'institut_plus_info': institute_names,'exact_institute' : exact_institut}
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the education: " + str(e))
        return {'programs': programmes, 'institut_plus_info': institute_names,'exact_institute' : exact_institut}

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
    try : 
        annot = annot_skills(resume_text,skill_extractor)
        skills = get_skills(annot)
        final_skills = check_constraints(skills)
        return final_skills
    except Exception as e:
      # Catch any other exceptions and log error message
        logging.error("Error while Extracting the skillls: " + str(e))
        return final_skills
def remove_accents(input_string):
    accents = {'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e', 'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E'}  # Add more mappings as needed
    
    for accent, replacement in accents.items():
        input_string = input_string.replace(accent, replacement)
    
    return input_string
def extract_years_of_experience(text):
    text2=remove_accents(text)
    years_of_experience = 0
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
        r'ans\s*d\'experience\s*:\s*(\d+)',
    ]
    years_of_experience = None

    for pattern in patterns:
        match = re.search(pattern, text2, re.IGNORECASE)
        if match:
            years_of_experience = match.group(1)
            break
    
    return years_of_experience


def extract_all_info(resume_text,skill_extractor) : 
    infos = dict() 
    try : 
        infos['number'] = extract_number(resume_text) 
        infos['email'] = extract_email(resume_text) 
        infos['education'] = extract_education(resume_text) 
        infos['skills'] = extract_skills(resume_text,skill_extractor)
        infos['year_of_experience'] = extract_years_of_experience(resume_text)
        return infos 
    except Exception as e:
        # Catch any other exceptions and log error message
        logging.error("Error while Extracting the informations: " + str(e))
        return infos