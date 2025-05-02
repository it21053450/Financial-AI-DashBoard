import React, { useState } from 'react';

function UploadForm({ onUpload, isLoading }) {
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const pdfFiles = selectedFiles.filter(file => file.type === 'application/pdf');
    
    if (pdfFiles.length !== selectedFiles.length) {
      setMessage('Please select only PDF files.');
    } else {
      setFiles(pdfFiles);
      setMessage(`${pdfFiles.length} file(s) selected.`);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setMessage('Please select at least one PDF file.');
      return;
    }
    onUpload(files);
  };

  return (
    <div className="upload-form">
      <h3>Upload Annual Reports</h3>
      <p className="upload-info">
        Upload John Keells Annual Reports (2019-2024) to analyze financial metrics.
      </p>
      
      <form onSubmit={handleSubmit}>
        <div className="file-input-container">
          <input
            type="file"
            id="pdfFiles"
            className="file-input"
            multiple
            accept=".pdf"
            onChange={handleFileChange}
            disabled={isLoading}
          />
          <label htmlFor="pdfFiles" className="file-input-label">
            Select PDF Files
          </label>
        </div>
        
        {message && <p className="file-message">{message}</p>}
        
        <button 
          type="submit" 
          className="upload-button" 
          disabled={isLoading || files.length === 0}
        >
          {isLoading ? 'Uploading...' : 'Upload and Process'}
        </button>
      </form>
    </div>
  );
}

export default UploadForm;