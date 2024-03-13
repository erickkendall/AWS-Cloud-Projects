# Test to use for Lambda function
#{
#  "sessionState": {
#    "intent": {
#      "name": "TranslateIntent",
#      "slots": {
#        "text": {
#          "value": {
#            "interpretedValue": "Hello",
#            "originalValue": "Hello"
#          }
#        },
#        "language": {
#          "value": {
#            "interpretedValue": "French",
#            "originalValue": "French"
#          }
#        }
#      }
#    }
#  }
#}
import boto3

def lambda_handler(event, context):
    try:
        input_text = event['sessionState']['intent']['slots']['text']['value']['interpretedValue'].strip()
        language_slot = event['sessionState']['intent']['slots']['language']['value']['interpretedValue'] 
        
        if not input_text:
            raise ValueError("Input text is empty")
        
        language_codes = {

            'French': 'fr',
            'Chinese': 'zh',
            'Russians': 'ru',
            'Japanese': 'ja',
            'Italian': 'it',
        }

        if language_slot not in language_codes:
            raise ValueError(f"Unsupported language: {language_slot}")
        
        target_language = language_codes[language_slot]

        target_client = boto3.client('translate')   

        response = target_client.translate_text(
            Text=input_text,
            SourceLanguageCode='auto',
            TargetLanguageCode=target_language
        )

        translated_text = response['TranslatedText']    

        lex_response = {
            "sessionState": {
              "dialogAction": {
                  "type" : "Close"
              },
              "intent" : {
                "name" : "TranslationIntent", #Add your Intent Name
                "state" : "Fulfilled"
              }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": translated_text
                }
            ]
        }
        return lex_response
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        lex_response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                    },
                "intent": {
                    "name": "TranslationIntent",
                    "state": "Failed",
                    "confirmationState": "None"
                    },
                "message": {
                    "contentType": "PlainText",
                    "content": error_message
                }
            }
        }
        return lex_response 
