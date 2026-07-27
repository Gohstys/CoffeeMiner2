# CoffeeMiner2

> ⚠️ **Strictly an educational and security-research project.**
> Proof of concept (PoC) of a *Man-in-the-Middle* attack with JavaScript
> injection. **This is not a functional or maintained product.** Read the
> [Legal & ethical notice](#-legal--ethical-notice) before anything else.

CoffeeMiner2 is a didactic reimplementation of the classic
[CoffeeMiner](https://arnaucode.com/blog/coffeeminer-hacking-wifi-cryptocurrency-miner.html),
the PoC that popularized the idea of "cryptojacking" on public WiFi networks. It
exists to **understand and demonstrate, in a controlled lab**, how an attacker on
the same local network can intercept HTTP traffic and inject arbitrary content.

The goal of this repository is to **learn**: how ARP spoofing works, why
cleartext HTTP traffic is insecure, and why HTTPS/HSTS mitigate this class of
attacks.

---

## 🔒 Legal & ethical notice

**READ THIS BEFORE RUNNING ANYTHING.**

- This software is published **solely for educational and defensive
  security-research purposes**. Its intent is didactic: to understand an attack
  technique in order to defend against it.
- Intercepting, modifying, or redirecting the network traffic of third parties
  **without their explicit consent is ILEGAL** in virtually every jurisdiction
  (in the US, the Computer Fraud and Abuse Act; in the EU, Directive 2013/40/EU;
  in Spain, arts. 197 and 264 of the Penal Code, among others).
- Run this tool **only** against systems and networks you own, or for which you
  hold **express written authorization** (for example, an isolated lab
  environment or a contracted penetration test).
- The author and contributors **accept no liability** for any misuse, damage,
  loss, or legal consequence arising from the use of this code. **All
  responsibility lies with whoever runs it.**
- Using this project implies acceptance of these terms. If you do not agree,
  **do not use it**.

> If your goal is to mine cryptocurrency, this is NOT the project: unauthorized
> mining on other people's machines is resource abuse and a crime. Use your own
> hardware.

---

## ⚙️ How it works

```
                        ┌──────────────┐
   Victim   ◄── ARP ───►│  Attacker    │◄── ARP ──►  Gateway / Router
 (same LAN)  spoofing   │ (CoffeeMiner)│  spoofing
                        └──────┬───────┘
                               │  The victim's traffic now flows through the attacker
                               ▼
           iptables redirects :80/:443 ──► mitmproxy (:8080, transparent)
                               │
                               ▼
          injector.py inserts <script src=".../m.js"> into every text/html response
                               │
                               ▼
                 httpServer.py serves the injected JavaScript
```

Components:

| File             | Role                                                                    |
|------------------|-------------------------------------------------------------------------|
| `coffeeMiner.py` | Orchestrator: enables IP forwarding, sets up the `iptables` rules, launches `arpspoof` per victim, the HTTP server, and `mitmdump`. |
| `injector.py`    | mitmproxy addon that injects a `<script>` tag into `text/html` responses. |
| `httpServer.py`  | Serves the JavaScript payload (`miner_script/m.js`).                     |
| `miner_script/m.js` | The JavaScript injected into the victim's pages.                     |
| `install.sh`     | Installs dependencies (`dsniff`, `mitmproxy`, `beautifulsoup4`).         |

---

## 📋 Requirements

- A Linux system for the attacker (tested on **Kali Linux**).
- `dsniff` (provides `arpspoof`), `mitmproxy` (`mitmdump`), `python3`,
  `beautifulsoup4`, and `xterm`.
- Attacker and victim(s) on the **same local network segment** (same broadcast
  domain).

```bash
chmod +x install.sh
sudo ./install.sh
```

---

## ▶️ Usage (your own lab only)

1. Create a `victims.txt` file with one IP per line (the machines **in your
   lab**):

   ```
   192.168.1.50
   192.168.1.51
   ```

2. Launch the attack, passing the gateway IP:

   ```bash
   sudo python3 coffeeMiner.py <GATEWAY_IP>
   ```

---

## 🐛 Project status & known issues

> **The project is paused indefinitely and does NOT work end to end.**
> The real state is documented here for transparency.

- **HTTPS / certificates (main open bug).** `httpServer.py` tries to bring up TLS
  but the paths are *hardcoded* to `/home/kali/Desktop/CoffeeMiner2/...` and
  **do not match each other**: the `certfile`/`keyfile` variables point to
  `cert.pem`/`key.pem`, while `load_cert_chain()` loads `certificate.crt`/
  `private.key`. None of those files are included in the repo either. As a result,
  the server won't start until you generate the certificates and unify the paths.
- **HTTP only.** Injection only affects cleartext HTTP traffic. Against HTTPS,
  HSTS, and modern sites the attack **does not succeed** (which is precisely the
  defensive lesson of the exercise).
- **Observed behavior.** In testing, the setup ends up **denying access to the IPs
  listed** in `victims.txt` (a DoS side effect of the spoofing/routing) instead of
  injecting the miner. The cause is under investigation.
- **Absolute paths.** `httpServer.py` and `coffeeMiner.py` assume fixed Kali paths
  (`/home/kali/Desktop/...`, `/usr/bin/mitmdump`). Adjust them to your environment.
- **mitmdump.** Must be reachable at `/usr/bin/mitmdump` (or edit the path in
  `coffeeMiner.py`).

---

## 🛡️ How to defend yourself (the real takeaway)

- Use **HTTPS everywhere** and enable **HSTS**; check for the padlock.
- Be wary of **public WiFi**; use a **VPN**.
- Enable **ARP spoofing** protection / *Dynamic ARP Inspection* on the switch when
  possible.
- Watch for **duplicate ARP entries** (`arp -a`) and unexpected traffic spikes.

---

## 📄 License

Released under the **MIT** license (see [`LICENSE`](LICENSE)). The MIT license
grants no permission whatsoever for illegal activities; see the
[Legal & ethical notice](#-legal--ethical-notice).
