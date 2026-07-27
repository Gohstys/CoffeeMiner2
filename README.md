# CoffeeMiner2

> ⚠️ **Proyecto exclusivamente educativo y de investigación en seguridad.**
> Prueba de concepto (PoC) de un ataque *Man-in-the-Middle* con inyección de
> JavaScript. **No es un producto funcional ni mantenido.** Lee la sección
> [Aviso legal y ético](#-aviso-legal-y-ético) antes de nada.

CoffeeMiner2 es una reimplementación con fines didácticos del clásico
[CoffeeMiner](https://arnaucode.com/blog/coffeeminer-hacking-wifi-cryptocurrency-miner.html),
la PoC que popularizó la idea de "cryptojacking" en redes WiFi públicas. Sirve
para **entender y demostrar en un laboratorio controlado** cómo un atacante en la
misma red local puede interceptar tráfico HTTP e inyectar contenido arbitrario.

El objetivo de este repositorio es **aprender**: cómo funciona el ARP spoofing,
por qué el tráfico HTTP en claro es inseguro, y por qué HTTPS/HSTS mitigan este
tipo de ataques.

---

## 🔒 Aviso legal y ético

**LEE ESTO ANTES DE EJECUTAR NADA.**

- Este software se publica **únicamente con fines educativos y de investigación
  en seguridad informática defensiva**. Su propósito es didáctico: comprender una
  técnica de ataque para poder defenderse de ella.
- Interceptar, modificar o redirigir el tráfico de red de terceros **sin su
  consentimiento explícito es ILEGAL** en la práctica totalidad de las
  jurisdicciones (en España, entre otros, arts. 197 y 264 del Código Penal; en la
  UE, Directiva 2013/40/UE; en EE. UU., la Computer Fraud and Abuse Act).
- Ejecuta esta herramienta **exclusivamente** contra equipos y redes de tu
  propiedad, o para los que dispongas de **autorización expresa y por escrito**
  (por ejemplo, un entorno de laboratorio aislado o un pentest contratado).
- El autor y los contribuidores **no se hacen responsables** de ningún uso
  indebido, daño, pérdida o consecuencia legal derivada del empleo de este código.
  **Toda la responsabilidad recae sobre quien lo ejecuta.**
- El uso de este proyecto implica la aceptación de estas condiciones. Si no estás
  de acuerdo, **no lo uses**.

> Si lo que buscas es minar criptomonedas, este NO es el proyecto: la minería no
> autorizada en equipos ajenos es abuso de recursos y un delito. Usa tu propio
> hardware.

---

## ⚙️ Cómo funciona

```
                        ┌──────────────┐
   Víctima  ◄── ARP ───►│  Atacante    │◄── ARP ──►  Gateway / Router
 (mismo LAN)  spoofing  │ (CoffeeMiner)│  spoofing
                        └──────┬───────┘
                               │  El tráfico de la víctima pasa por el atacante
                               ▼
           iptables redirige :80/:443 ──► mitmproxy (:8080, transparente)
                               │
                               ▼
          injector.py inserta <script src=".../m.js"> en cada respuesta text/html
                               │
                               ▼
                 httpServer.py sirve el JavaScript inyectado
```

Componentes:

| Fichero          | Función                                                                 |
|------------------|-------------------------------------------------------------------------|
| `coffeeMiner.py` | Orquestador: habilita IP forwarding, monta las reglas `iptables`, lanza `arpspoof` por víctima, el servidor HTTP y `mitmdump`. |
| `injector.py`    | Addon de mitmproxy que inyecta una etiqueta `<script>` en las respuestas `text/html`. |
| `httpServer.py`  | Sirve el payload JavaScript (`miner_script/m.js`).                       |
| `miner_script/m.js` | El JavaScript que se inyecta en las páginas de la víctima.            |
| `install.sh`     | Instala dependencias (`dsniff`, `mitmproxy`, `beautifulsoup4`).          |

---

## 📋 Requisitos

- Un sistema Linux para el atacante (probado en **Kali Linux**).
- `dsniff` (aporta `arpspoof`), `mitmproxy` (`mitmdump`), `python3`,
  `beautifulsoup4` y `xterm`.
- Atacante y víctima(s) en el **mismo segmento de red local** (mismo dominio de
  broadcast).

```bash
chmod +x install.sh
sudo ./install.sh
```

---

## ▶️ Uso (solo en laboratorio propio)

1. Crea un fichero `victims.txt` con una IP por línea (los equipos **de tu
   laboratorio**):

   ```
   192.168.1.50
   192.168.1.51
   ```

2. Lanza el ataque indicando la IP del gateway:

   ```bash
   sudo python3 coffeeMiner.py <IP_DEL_GATEWAY>
   ```

---

## 🐛 Estado del proyecto y problemas conocidos

> **El proyecto está pausado indefinidamente y NO funciona de forma completa.**
> Se documenta el estado real por transparencia.

- **HTTPS / certificados (principal bug abierto).** `httpServer.py` intenta
  levantar TLS pero las rutas están *hardcodeadas* a
  `/home/kali/Desktop/CoffeeMiner2/...` y **no coinciden entre sí**: las variables
  `certfile`/`keyfile` apuntan a `cert.pem`/`key.pem`, mientras que
  `load_cert_chain()` carga `certificate.crt`/`private.key`. Además ninguno de
  esos ficheros se incluye en el repo. Resultado: el servidor no arranca hasta
  generar los certificados y unificar las rutas.
- **Solo HTTP.** La inyección únicamente afecta a tráfico HTTP en claro. Frente a
  HTTPS, HSTS y sitios modernos el ataque **no prospera** (que es precisamente la
  lección defensiva del ejercicio).
- **Comportamiento observado.** En pruebas, el montaje llega a **denegar el
  acceso a las IPs listadas** en `victims.txt` (efecto DoS por el spoofing/routing)
  en lugar de inyectar el minero. La causa está bajo investigación.
- **Rutas absolutas.** `httpServer.py` y `coffeeMiner.py` asumen rutas fijas de
  Kali (`/home/kali/Desktop/...`, `/usr/bin/mitmdump`). Ajústalas a tu entorno.
- **mitmdump.** Debe estar accesible en `/usr/bin/mitmdump` (o edita la ruta en
  `coffeeMiner.py`).

---

## 🛡️ Cómo defenderse (lo que de verdad deberías aprender)

- Usa **HTTPS en todas partes** y activa **HSTS**; verifica el candado.
- Desconfía de las **redes WiFi públicas**; usa una **VPN**.
- Habilita protección contra **ARP spoofing** / *Dynamic ARP Inspection* en el
  switch cuando sea posible.
- Vigila **entradas ARP duplicadas** (`arp -a`) y picos de tráfico inesperados.

---

## 📄 Licencia

Distribuido bajo licencia **MIT** (ver [`LICENSE`](LICENSE)). La licencia MIT no
concede permiso alguno para actividades ilegales; consulta el
[Aviso legal y ético](#-aviso-legal-y-ético).
