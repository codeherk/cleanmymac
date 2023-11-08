import os
import csv
import logging
import time

def delete_files_in_directory(directory, writer):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.stat(file_path).st_size
                writer.writerow([file_path,file_size])
                os.remove(file_path)
                logging.debug(f"Deleted file: {file_path}")
                count = count + 1
            except Exception as e:
                logging.error(f"Failed to delete file: {file_path}\nError: {str(e)}")
    return count

if __name__ == '__main__':
    t = time.localtime()
    current_time = time.strftime("%m%d%y-%H%M%S", t)
    file_prefix = "{}-{}-delcache".format(os.getlogin(), current_time)
    logging.basicConfig(filename=f'{file_prefix}.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    
    cache_directory = '/Users/codeherk/Library/Caches/'  # Replace with the actual path to your 'Library/Caches/' directory

    if os.path.exists(cache_directory):
        try:
            # Create CSV file 
            csv_filename = f"{file_prefix}.csv"
            logging.debug(f"Creating file {csv_filename}.")
            with open(csv_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["file", "size"])
                file_count = delete_files_in_directory(cache_directory, writer)
                logging.info(f"All {file_count} files in subfolders of 'Library/Caches/' have been deleted.")
        except Exception as e:
            logging.error(str(e))
    else:
        logging.error(f"Directory '{cache_directory}' does not exist.")
    
    logging.info(f"Logs can viewed in {file_prefix}.log")