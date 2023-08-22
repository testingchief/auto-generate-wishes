![Build](http://img.shields.io/badge/release-1.0-GREEN.svg)
![Twitter](http://img.shields.io/badge/@testingchief--lightgrey?logo=twitter&amp;style=social)

# auto-generate-wishes
Fetch a random image from Unsplash using a search query and add custom text to the image.

To run the script, run this command.
> python3 scripts/generate-wishes.py 'birthday' 'UNSPLASH_KEY' 'SENDER_NAME'

![Auto Generated Image](https://github.com/testingchief/auto-generate-wishes/blob/main/images/wish.png?raw=true)

Sample Pipeline Script
- Install requirements
- Get a random image from Unsplash
- Add text to the downloaded image
- Upload to Slack
  
> pipeline {
    agent any
    parameters {
        string defaultValue: 'Siva Ganesan', description: 'Sender name', name: 'SENDER', trim: true
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
                sh "python3 scripts/generate-wishes.py 'birthday' '${params.UNSPLASH_KEY}' '${params.SENDER}'"
            }
        } 
        stage('upload-image-to-slack') {
            steps {
                slackUploadFile filePath: 'images/wish.png', credentialId: 'xxx', initialComment: 'auto-generated image for the day!'
            }
        }
    }
}
