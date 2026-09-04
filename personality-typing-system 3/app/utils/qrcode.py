"""QR Code Generation for Survey Access"""
import qrcode
import uuid
from io import BytesIO
from typing import Tuple, List
import os


class QRCodeGenerator:
    """Generate QR Codes for Survey Access"""
    
    BASE_URL = "https://personality-typing-system.onrender.com"  # Change for production
    
    @staticmethod
    def generate_qr_code(
        survey_id: str, 
        survey_type: str = "student",
        base_url: str = None
    ) -> Tuple[BytesIO, str]:
        """
        Generate QR Code for survey
        
        Args:
            survey_id: UUID of survey
            survey_type: 'student' or 'enterprise'
            base_url: Custom base URL (optional)
            
        Returns:
            Tuple[BytesIO, str]: QR Code image and survey URL
            
        Example:
            >>> img, url = QRCodeGenerator.generate_qr_code("survey-123", "student")
            >>> print(url)
            https://personality-typing-system.onrender.com?survey_id=survey-123&type=student
        """
        if base_url is None:
            base_url = QRCodeGenerator.BASE_URL
        
        # URL where survey can be accessed
        survey_url = f"{base_url}?survey_id={survey_id}&type={survey_type}"
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(survey_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return img_io, survey_url
    
    @staticmethod
    def generate_multiple_qr_codes(
        survey_ids: List[str], 
        output_dir: str = "./qr_codes",
        survey_type: str = "student"
    ) -> List[str]:
        """
        Generate batch QR codes and save to files
        
        Args:
            survey_ids: List of survey IDs
            output_dir: Directory to save QR codes
            survey_type: Type of survey
            
        Returns:
            List[str]: URLs for all surveys
        """
        os.makedirs(output_dir, exist_ok=True)
        
        urls = []
        for survey_id in survey_ids:
            img_io, url = QRCodeGenerator.generate_qr_code(survey_id, survey_type)
            
            # Save to file
            filename = f"{output_dir}/survey_{survey_id}.png"
            with open(filename, 'wb') as f:
                f.write(img_io.getvalue())
            
            urls.append(url)
        
        return urls
    
    @staticmethod
    def generate_html_qr_card(survey_id: str, survey_type: str = "student") -> str:
        """
        Generate HTML card with QR code for embedding
        
        Args:
            survey_id: Survey ID
            survey_type: Type of survey
            
        Returns:
            str: HTML card
        """
        img_io, url = QRCodeGenerator.generate_qr_code(survey_id, survey_type)
        
        # Convert to base64
        import base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        html = f"""
        <div style="text-align: center; padding: 20px; border: 2px solid #ddd; border-radius: 10px;">
            <h3>📋 Survey QR Code</h3>
            <img src="data:image/png;base64,{img_base64}" style="width: 300px; height: 300px;">
            <p><strong>Survey ID:</strong> {survey_id}</p>
            <p><small>or visit: <a href="{url}" target="_blank">{url}</a></small></p>
        </div>
        """
        return html
