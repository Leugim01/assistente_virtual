import speech_recognition as sr #pip install SpeechRecognition / pip install pyaudio
import re
import webbrowser
import pyttsx3 #pip install pyttsx3
from googlesearch import search #pip install googlesearch-python
import requests #pip install request
from bs4 import BeautifulSoup #pip install bs4
from PIL import Image #pip install Pillow

nome = ""

while(True):

    mic = sr.Recognizer()

    with sr.Microphone() as source:
        engine = pyttsx3.init()
        engine.setProperty('voice', "com.apple.speech.synthesis.voice.luciana")
        mic.adjust_for_ambient_noise(source)

        print("Fale alguma coisa...")

        audio = mic.listen(source)

        try:
            frase = mic.recognize_google(audio,language='pt-BR')
            
            if(re.search(r'\b' + "ajuda" + r'\b',format(frase))):
                engine.say("Ajuda")
                engine.runAndWait()
                print("Algo sobre ajuda")
            
            elif(re.search(r'\b' + "meu nome é " + r'\b',format(frase))):
                t = re.search('meu nome é (.*)',format(frase))
                nome = t.group(1)
                print("Seu nome é "+nome)
                engine.say("Nome falado foi "+nome);
                engine.runAndWait()

            elif(re.search(r'\b' + "navegador" + r'\b',format(frase))):
                webbrowser.open("https://www.google.com/")
                engine.say("Abrindo site");
                engine.runAndWait()

            elif(re.search(r'\b' + "pesquisar" + r'\b',format(frase))):
                webbrowser.open("https://www.google.com/search?q="+frase)
                engine.say("Pesquisando");
                engine.runAndWait()
            
            elif(re.search(r'\b' + "estudar Odonto" + r'\b',format(frase))):
                webbrowser.open("https://manu-studies.netlify.app")
                engine.say("Vamos lá");
                engine.runAndWait()
                
            elif(re.search(r'\b' + "portal do aluno" + r'\b',format(frase))):
                webbrowser.open("https://novoportal.cruzeirodosul.edu.br/?empresa=udf&blackboard=false")
                engine.say("Abrindo portal do aluno");
                engine.runAndWait()

            elif(re.search(r'\b' + "horas são" + r'\b',format(frase))):
                engine.say("São 11 e 25")
                engine.runAndWait()
                print("Horario")

            elif(re.search(r'\b' + "baixar" + r'\b',format(frase))):
                run = True
                directory = "C:/Users/adm/Desktop/Teste"
                print('')
                search = (frase)
                print('')
                num_of_img = 10
                print('')
                print('Downloading...')
                print('')
                links_list = []
                img_list = []
                img_index = 0
                page_number = (num_of_img // 20) * 20

                url1 = f'https://www.google.com/search?q={search}&hl=pt-BR&gbv=1&source=lnms&tbm=isch&sa=X&ved=2ahUKEwipwcKTxOfrAhUUDrkGHZ3kB5kQ_AUoAXoECB8QAw&sfr=gws&sei=g8xeX6WWO4KI5OUP1Ne2sAQ'  
                req = requests.get(url1)
                soup = BeautifulSoup(req.text, 'html.parser')

                for img in soup.find_all('img')[1:]: #getting all the 'img' tag from the html file, excelpt the google icon
                        if img_index == num_of_img: 
                            break
                        else:
                            links_list.append(img.get('src'))
                            img_index += 1

                for links in links_list:
                        img_list.append(requests.get(links)) #acessing the images page and storing the link in a list

                for i, img in enumerate(img_list): #converting the images into byte
                        with open(f'{directory}/{search}_{i}.png', 'wb') as f: #wb = write byte
                            f.write(img.content)

                for pages in range(20, page_number + 20, 20):
                        img_list = []
                        links_list = []

                        if img_index == num_of_img:
                            break
                        else:
                            urln = f'https://www.google.com/search?q={search}&hl=pt-BR&gbv=1&tbm=isch&ei=78xeX5PTGc_Z5OUPrsyA0A0&start={pages}&sa=N' 
                            req = requests.get(urln)
                            soup = BeautifulSoup(req.text, 'html.parser')

                            for img in soup.find_all('img')[1:]:
                                if img_index == num_of_img:
                                    break
                                else:
                                    links_list.append(img.get('src'))
                                    img_index += 1

                            for links in links_list:
                                img_list.append(requests.get(links))

                            for i, img in enumerate(img_list):
                                with open(f'{directory}/{search}_{i + img_index - len(links_list)}.png', 'wb') as f: #wb = write byte
                                    f.write(img.content)

                                   
                        
                print('DONE!')
                print('')
                if img_index < num_of_img:
                        print(f"It was only possible to download {img_index} images")
                        print('')
                if img_index == 0:
                        print("Unfortunately we didn't find any image to download")
                        print('')
                    
                engine.say("Baixando");
                engine.runAndWait()

                images = [
                    Image.open("C:/Users/adm/Desktop/Teste/" + f)
                    for f in [(frase)+"_0.png", (frase)+"_1.png", (frase)+"_2.png", (frase)+"_3.png", (frase)+"_4.png", (frase)+"_5.png", (frase)+"_6.png", (frase)+"_7.png", (frase)+"_8.png", (frase)+"_9.png"]
                ]

                pdf_path = "C:/Users/adm/Desktop/Teste/Seu_PDF.pdf"
                    
                images[0].save(
                    pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
                )


            print('Voce falou: ' + frase)
        
        except sr.UnknownValueError:
            print("Ops, algo deu errrado")
