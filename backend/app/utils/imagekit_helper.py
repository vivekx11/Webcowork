"""
ImageKit integration helper
"""
import os
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

class ImageKitHelper:
    """Helper class for ImageKit operations"""
    
    def __init__(self):
        self.imagekit = ImageKit(
            private_key=os.getenv('IMAGEKIT_PRIVATE_KEY'),
            public_key=os.getenv('IMAGEKIT_PUBLIC_KEY'),
            url_endpoint=os.getenv('IMAGEKIT_URL_ENDPOINT')
        )
    
    def upload_image(self, file, file_name, folder='products'):
        """
        Upload image to ImageKit
        
        Args:
            file: File object or base64 string
            file_name: Name for the file
            folder: Folder path in ImageKit
        
        Returns:
            dict: Upload response with url and file_id
        """
        try:
            options = UploadFileRequestOptions(
                folder=f"/{folder}/",
                use_unique_file_name=True,
                response_fields=['file_id', 'url', 'name']
            )
            
            result = self.imagekit.upload_file(
                file=file,
                file_name=file_name,
                options=options
            )
            
            if result.response_metadata.http_status_code == 200:
                return {
                    'success': True,
                    'url': result.url,
                    'file_id': result.file_id,
                    'name': result.name
                }
            else:
                return {
                    'success': False,
                    'error': 'Upload failed'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_image(self, file_id):
        """
        Delete image from ImageKit
        
        Args:
            file_id: ImageKit file ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            result = self.imagekit.delete_file(file_id)
            return result.response_metadata.http_status_code == 204
        except Exception as e:
            print(f"Error deleting image: {str(e)}")
            return False
    
    def get_image_url(self, file_path, transformations=None):
        """
        Get ImageKit URL with optional transformations
        
        Args:
            file_path: Path to the file in ImageKit
            transformations: List of transformation objects
        
        Returns:
            str: Image URL
        """
        try:
            url = self.imagekit.url({
                'path': file_path,
                'transformation': transformations or []
            })
            return url
        except Exception as e:
            print(f"Error generating URL: {str(e)}")
            return None

# Create a singleton instance
imagekit_helper = ImageKitHelper()
