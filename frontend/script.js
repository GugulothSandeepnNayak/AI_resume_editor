// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const statusCard = document.getElementById('statusCard');
const statusIcon = document.getElementById('statusIcon');
const statusText = document.getElementById('statusText');
const fileUploadArea = document.getElementById('fileUploadArea');
const resumeFile = document.getElementById('resumeFile');
const uploadBtn = document.getElementById('uploadBtn');
const jobDescription = document.getElementById('jobDescription');
const tailorBtn = document.getElementById('tailorBtn');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const copyBtn = document.getElementById('copyBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');
const toastContainer = document.getElementById('toastContainer');

// State
let resumeUploaded = false;
let currentResumeContent = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkSystemStatus();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // File upload area
    fileUploadArea.addEventListener('click', () => resumeFile.click());
    fileUploadArea.addEventListener('dragover', handleDragOver);
    fileUploadArea.addEventListener('dragleave', handleDragLeave);
    fileUploadArea.addEventListener('drop', handleDrop);
    
    // File input
    resumeFile.addEventListener('change', handleFileSelect);
    
    // Upload button
    uploadBtn.addEventListener('click', uploadResume);
    
    // Job description textarea
    jobDescription.addEventListener('input', validateForm);
    
    // Tailor button
    tailorBtn.addEventListener('click', tailorResume);
    
    // Copy button
    copyBtn.addEventListener('click', copyResults);
}

// Check system status
async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/check-ollama-status/`);
        const data = await response.json();
        
        if (data.ollama_running) {
            updateStatus('success', 'System ready! Ollama is running and models are available.');
            enableUpload();
        } else {
            updateStatus('error', 'Ollama is not running. Please start Ollama and pull required models.');
        }
    } catch (error) {
        updateStatus('error', 'Cannot connect to backend server. Please ensure the server is running.');
        console.error('Status check failed:', error);
    }
}

// Update status display
function updateStatus(type, message) {
    statusText.textContent = message;
    
    if (type === 'success') {
        statusIcon.className = 'fas fa-check-circle';
        statusIcon.style.color = '#28a745';
        statusCard.style.borderLeft = '4px solid #28a745';
    } else if (type === 'error') {
        statusIcon.className = 'fas fa-exclamation-circle';
        statusIcon.style.color = '#dc3545';
        statusCard.style.borderLeft = '4px solid #dc3545';
    } else if (type === 'warning') {
        statusIcon.className = 'fas fa-exclamation-triangle';
        statusIcon.style.color = '#ffc107';
        statusCard.style.borderLeft = '4px solid #ffc107';
    }
}

// Enable upload functionality
function enableUpload() {
    uploadBtn.disabled = false;
    fileUploadArea.style.cursor = 'pointer';
}

// File upload handlers
function handleDragOver(e) {
    e.preventDefault();
    fileUploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    fileUploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    // Validate file type
    const allowedTypes = ['.txt', '.md', '.pdf'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(fileExtension)) {
        showToast('Please select a .txt, .md, or .pdf file.', 'error');
        return;
    }
    
    // Update UI to show selected file
    const uploadContent = fileUploadArea.querySelector('.upload-content');
    uploadContent.innerHTML = `
        <i class="fas fa-file-alt"></i>
        <p><strong>${file.name}</strong></p>
        <small>${(file.size / 1024).toFixed(1)} KB</small>
    `;
    
    // Enable upload button
    uploadBtn.disabled = false;
    
    // Store file for upload
    currentResumeFile = file;
}

// Upload resume
async function uploadResume() {
    if (!currentResumeFile) {
        showToast('Please select a resume file first.', 'error');
        return;
    }
    
    showLoading('Uploading and processing your resume...');
    
    try {
        const formData = new FormData();
        formData.append('resume_file', currentResumeFile);
        
        const response = await fetch(`${API_BASE_URL}/ingest-resume/`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to upload resume');
        }
        
        const data = await response.json();
        resumeUploaded = true;
        validateForm();
        
        showToast('Resume uploaded and processed successfully!', 'success');
        hideLoading();
        
    } catch (error) {
        hideLoading();
        showToast(`Upload failed: ${error.message}`, 'error');
        console.error('Upload error:', error);
    }
}

// Validate form
function validateForm() {
    const hasJobDescription = jobDescription.value.trim().length > 0;
    tailorBtn.disabled = !(resumeUploaded && hasJobDescription);
}

// Tailor resume
async function tailorResume() {
    const jobDescText = jobDescription.value.trim();
    
    if (!jobDescText) {
        showToast('Please enter a job description.', 'error');
        return;
    }
    
    if (!resumeUploaded) {
        showToast('Please upload a resume first.', 'error');
        return;
    }
    
    showLoading('Analyzing job description and tailoring your resume...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/tailor-resume/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: jobDescText
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to tailor resume');
        }
        
        const data = await response.json();
        displayResults(data.tailored_resume);
        hideLoading();
        
        showToast('Resume tailored successfully!', 'success');
        
    } catch (error) {
        hideLoading();
        showToast(`Tailoring failed: ${error.message}`, 'error');
        console.error('Tailoring error:', error);
    }
}

// Display results
function displayResults(data) {
    // Handle both old format (string) and new format (object)
    let tailoredResume, atsScore;
    
    if (typeof data === 'string') {
        tailoredResume = data;
        atsScore = null;
    } else {
        tailoredResume = data.tailored_resume;
        atsScore = data.ats_score;
    }
    
    // Display tailored resume
    resultsContent.textContent = tailoredResume;
    
    // Display ATS score if available
    if (atsScore) {
        displayATSScore(atsScore);
    }
    
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Display ATS score
function displayATSScore(atsScore) {
    // Update overall score
    document.getElementById('scoreNumber').textContent = atsScore.overall_score;
    
    // Update individual scores with animations
    updateScoreBar('keywordScore', atsScore.keyword_score);
    updateScoreBar('skillScore', atsScore.skill_score);
    updateScoreBar('experienceScore', atsScore.experience_score);
    updateScoreBar('formatScore', atsScore.format_score);
    
    // Update score values
    document.getElementById('keywordScoreValue').textContent = `${Math.round(atsScore.keyword_score)}%`;
    document.getElementById('skillScoreValue').textContent = `${Math.round(atsScore.skill_score)}%`;
    document.getElementById('experienceScoreValue').textContent = `${Math.round(atsScore.experience_score)}%`;
    document.getElementById('formatScoreValue').textContent = `${Math.round(atsScore.format_score)}%`;
    
    // Display analysis
    const analysisDiv = document.getElementById('atsAnalysis');
    analysisDiv.innerHTML = `
        <h3><i class="fas fa-search"></i> Detailed Analysis</h3>
        <p>${atsScore.analysis}</p>
    `;
    
    // Display recommendations
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = `
        <h3><i class="fas fa-lightbulb"></i> Recommendations</h3>
        <ul>
            ${atsScore.recommendations.map(rec => `<li>${rec}</li>`).join('')}
        </ul>
    `;
    
    // Show missing keywords if any
    if (atsScore.missing_keywords && atsScore.missing_keywords.length > 0) {
        recommendationsDiv.innerHTML += `
            <h4 style="margin-top: 15px; color: #dc3545;">Missing Keywords:</h4>
            <p style="color: #666; font-size: 0.9rem;">${atsScore.missing_keywords.slice(0, 10).join(', ')}${atsScore.missing_keywords.length > 10 ? '...' : ''}</p>
        `;
    }
}

// Update score bar with animation
function updateScoreBar(elementId, score) {
    const scoreBar = document.getElementById(elementId);
    const percentage = Math.min(score, 100);
    
    // Animate the score bar
    setTimeout(() => {
        scoreBar.style.width = `${percentage}%`;
    }, 100);
}

// Copy results
async function copyResults() {
    try {
        await navigator.clipboard.writeText(resultsContent.textContent);
        showToast('Resume copied to clipboard!', 'success');
        
        // Visual feedback
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        }, 2000);
        
    } catch (error) {
        showToast('Failed to copy to clipboard', 'error');
        console.error('Copy error:', error);
    }
}

// Loading overlay
function showLoading(message) {
    loadingText.textContent = message;
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

// Toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <i class="fas ${getToastIcon(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
    
    // Remove on click
    toast.addEventListener('click', () => toast.remove());
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showToast('An unexpected error occurred. Please try again.', 'error');
});

// Network status monitoring
window.addEventListener('online', function() {
    showToast('Connection restored', 'success');
    checkSystemStatus();
});

window.addEventListener('offline', function() {
    showToast('No internet connection', 'warning');
    updateStatus('error', 'No internet connection. Some features may not work.');
}); 