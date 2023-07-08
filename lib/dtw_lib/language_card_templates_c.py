from string import Template

SRC = 'target_language'
DES = 'destination_language'
FONT_SIZE_SMALL_PX = 18
FONT_SIZE_PX = 23
MAIN_FONT_SIZE_PX = 25

FRONT = '''
 <b>{{English (Simplified Translation)}}<br></b><br>
<span class="timer" id="s2"><span>
<script>
function countdown( elementName, minutes, seconds )
{
    var element, endTime, hours, mins, msLeft, time;

    function twoDigits( n )
    {
        return (n <= 9 ? "0" + n : n);
    }

    function updateTimer()
    {
        msLeft = endTime - (+new Date);
        if ( msLeft < 1000 ) {
            element.innerHTML = "Countdown's Over!";
        } else {
            time = new Date( msLeft );
            hours = time.getUTCHours();
            mins = time.getUTCMinutes();
            element.innerHTML = (hours ? hours + ':' + twoDigits( mins ) : mins) + ':' + twoDigits( time.getUTCSeconds() );
            setTimeout( updateTimer, time.getUTCMilliseconds() + 500 );
        }
    }

    element = document.getElementById( elementName );
    endTime = (+new Date) + 1000 * (60*minutes + seconds) + 500;
    updateTimer();
}

countdown("s2", 0, 5 );//2nd value is the minute, 3rd is the seconds
</script>
</u>'''

BACK = ''' <b>{{English (Simplified Translation)}}</b>
<br>
<hr>
{{''' + DES + '''}}<br>
</b>
<div class="tips"> {{Tips}} </div>
{{Audio}}
<br>
<div class = "sentence">
   {{Example Sentences (Translation)}}
</div>
<br>
    {{Picture}}
'''
STYLE = '''
.card {
 font-family:Consolas;
 font-size: '''+str(MAIN_FONT_SIZE_PX)+'''px;
 text-align: Center;
 color: g;
 background-color: white;
}

.center {
    margin: auto;
    width: 60%;
    border: 3px solid #73AD21;
    padding: 10px;
    text-align: left;
    font-size: '''+str(FONT_SIZE_PX)+'''px;
}

.tips {
text-align:center;
font-size:'''+str(FONT_SIZE_SMALL_PX)+'''px;
}

.sentence {
font-size:'''+str(FONT_SIZE_PX)+'''px;
font-family: arial;
text-align:left
}'''

def get_front() -> str:
    front = FRONT
    return front


def get_back(dest: str) -> str:
    back = BACK.replace(DES, dest.capitalize())
    return back


def get_style() -> str:
    style = STYLE
    return style
