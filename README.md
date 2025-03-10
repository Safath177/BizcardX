# BizCard Extractor

BizCard Extractor is a robust and user-friendly web application designed to extract, manage, and modify data from business cards effortlessly. Leveraging Optical Character Recognition (OCR) technology, this tool simplifies the process of digitizing and organizing business card information.

## Key Features
- **Upload and Extract**: Easily upload images of business cards in formats like PNG, JPG, and JPEG. Extract textual information using advanced OCR (EasyOCR).
- **Data Management**:
  - Save extracted data in a structured database.
  - Preview the data in a tabular format and modify it as needed.
  - Delete specific entries directly from the application.
- **Robust Technology**: The app employs SQLite for reliable data storage and management.

## How It Works
1. **Image Upload**: Upload an image of a business card.
2. **Text Extraction**: The app extracts textual information, including Name, Designation, Contact Details, Address, Email, and more, using EasyOCR.
3. **Data Display**: The extracted information is displayed in a tabular format for easy viewing.
4. **Database Operations**:
   - Save: Store the extracted data in a SQLite database.
   - Preview: View all stored entries from the database.
   - Modify: Edit the details of an existing entry.
   - Delete: Remove entries based on specific details.

## Technologies Used
- **Streamlit**: For creating an interactive web-based application.
- **EasyOCR**: For text extraction from images.
- **PIL (Pillow)**: For image processing.
- **SQLite**: For storing and managing extracted data.


## Application Workflow
The application consists of three primary tabs:

### Home:

Learn about the app's features and technologies.

### Upload and Modify:

Upload business card images and extract textual data.

Save, preview, or modify the extracted data.

### Delete:

Delete specific entries from the database based on provided filters.

## Contact:
If you have any questions or suggestions, feel free to contact me at alisafath@gmail.com



