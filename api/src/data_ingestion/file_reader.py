import sys
sys.path.append('..')
from src.exception import CustomException
from src.logger import logging
from tika import parser
from src.data_preprocessing.resume_preprocessing import remove_first_lines,remove_accents
def read_files(file_list,path):
  print("reading the files")
  """Reads a list of files and ignores the files that throw exceptions."""
  data = []
  for file in file_list:
    try:
        text = read_file(file,path)
        if ( text !=None ) : 
            data.append(text)
            logging.info(f"File {file} loaded successfully")
        else : 
            logging.error(f"File {file} is encrypted " + str(e))

    
    except Exception as e:
      # Catch any other exceptions and log error message
      logging.error("Error while reading the file: " + str(e))
    logging.info("Files transformed succesfully")
  print("finished reading them")
  return data

def read_file(file,path):
  """Reads a file and returns the content."""
  try:
    with open(path+'/'+file, "rb") as f:
      binary_data = f.read()
    parsed_pdf = parser.from_file(path+'/'+file)
    non_accent = remove_accents(parsed_pdf['content'].lower())
    return {'content':remove_first_lines(non_accent),"name":file,"binary":binary_data}
  except Exception as e:
    # Catch any other exceptions and log error message
    logging.error("Error while reading the file: " + str(e))
    return None
