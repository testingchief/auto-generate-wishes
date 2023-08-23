![Build](http://img.shields.io/badge/release-1.0-GREEN.svg)
![Twitter](http://img.shields.io/badge/@testingchief--lightgrey?logo=twitter&amp;style=social)

# auto-generate-wishes
Fetch a random image from Unsplash using a search query and add custom text to the image.

To run the script, run this command.
> python3 scripts/generate-wishes.py 'birthday' 'UNSPLASH_KEY' 'SENDER_NAME' ' '

> python3 scripts/generate-wishes.py 'anniversary' 'UNSPLASH_KEY' 'SENDER_NAME' 'Happy anniversary!!!'

![Auto Generated Image](https://github.com/testingchief/auto-generate-wishes/blob/main/images/wish.png?raw=true)

Sample Pipeline Script
- Install requirements
- Get a random image from Unsplash
- Add text to the downloaded image
- Upload to Slack
  
```
 pipeline {
    agent any
    parameters {
        string defaultValue: 'Testing Chief', description: 'Sender name', name: 'SENDER', trim: true
        string defaultValue: 'birthday', description: 'Search query', name: 'SEARCH', trim: true
        string defaultValue: ' ', description: 'Custom message', name: 'MESSAGE'
    }
    stages {
        stage('git') {
            steps {
                git branch: 'main', url: 'https://github.com/testingchief/auto-generate-wishes.git'
            }
        } 
        stage('install-reqs') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('generate-image') {
            steps {
                sh "python3 scripts/generate-wishes.py '${params.SEARCH}' '${params.UNSPLASH_KEY}' '${params.SENDER}' '${params.MESSAGE}'"
            }
        } 
        stage('upload-image-to-slack') {
            steps {
                slackUploadFile filePath: 'images/wish.png', credentialId: 'xxx', initialComment: 'auto-generated image for the day!'
            }
        }
    }
}
```
