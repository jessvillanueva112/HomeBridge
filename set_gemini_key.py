
import os
import json
import getpass

def set_gemini_key():
    print("HomeBridge - Set Gemini API Key")
    print("---------------------------------")
    print("This script will help you set up your Google Gemini API key.")
    print("You can get a key from https://makersuite.google.com/")
    print()
    
    # Get API key from user (using getpass for security)
    api_key = getpass.getpass("Enter your Gemini API Key: ")
    
    if not api_key.strip():
        print("Error: API key cannot be empty")
        return False
    
    try:
        # Check if we're in Replit environment
        if os.path.exists("/.replit"):
            # Set the key in Replit Secrets
            print("Setting API key in Replit Secrets...")
            
            # This approach depends on how Replit exposes the Secrets API
            # For now, just guide the user to do it manually
            print("\nPlease set GEMINI_API_KEY in Replit Secrets:")
            print("1. Click on the lock icon in the left sidebar")
            print("2. Click 'Add new secret'")
            print("3. Set key as 'GEMINI_API_KEY' and value as your API key")
            print("\nNote: This will keep your API key secure.")
            
            # For demonstration only - set in current environment
            os.environ["GEMINI_API_KEY"] = api_key
            
            return True
        else:
            # Not in Replit, use .env file
            with open(".env", "a+") as f:
                f.write(f"\nGEMINI_API_KEY={api_key}\n")
            
            print("API key has been saved to .env file")
            print("Make sure to load this file before running the application")
            
            # Also set in current environment
            os.environ["GEMINI_API_KEY"] = api_key
            
            return True
    
    except Exception as e:
        print(f"Error saving API key: {str(e)}")
        return False

if __name__ == "__main__":
    set_gemini_key()
