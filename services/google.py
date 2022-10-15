from unicodedata import name
from gtts import gTTS
from pydub import AudioSegment

def converter(v_data,language = 'en'):
    for i in v_data:
        instruction=i.instruction
        myobj = gTTS(text=instruction, lang=language, slow=False)
        name=str(i.r_id_id)+str(i.seq_no)
        myobj.save("media/"+name+".mp3")
    
    second_of_silence = AudioSegment.silent(duration=1000) 
    recipe_voice = AudioSegment.from_mp3("media/"+str(v_data[0].r_id_id)+"1.mp3")

    v_data=v_data[1:]
    for i in v_data:
        voice = AudioSegment.from_mp3("media/"+str(i.r_id_id)+str(i.seq_no)+".mp3")
        hours,min,sec = [int( x ) for x in i.time_stamp.split(":")]
        milisec=(hours*3600+min*60+sec)*1000
        silence = AudioSegment.silent(duration=milisec)
        recipe_voice += silence+voice 
    recipe_voice.export("media/recpie"+str(v_data[0].r_id_id)+".mp3")
    return "recpie"+str(v_data[0].r_id_id)+".mp3"