import zipfile


class ZipFileExtractor:
    def unzip_file(zip_file, extract_to):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_to)