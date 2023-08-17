from src.data_ingestion.file_reader import read_file 
path = 'data/raw_data'
text_file = read_file('rayen_data.pdf',path)
print(text_file)