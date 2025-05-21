document.getElementById("formulario").addEventListener("submit", async function (e) {
    e.preventDefault();

    const dados = Object.fromEntries(new FormData(this).entries());

    try {
        const resp = await fetch("http://127.0.0.1:8000/cliente/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const respostaTexto = await resp.text(); // Lê a resposta como texto puro

        if (!resp.ok) {
            try {
                const erro = JSON.parse(respostaTexto);
                document.getElementById("resposta").innerText = `Erro: ${erro.detail}`;
            } catch (jsonErro) {
                // Não era JSON, mostra texto cru
                document.getElementById("resposta").innerText = `Erro: ${respostaTexto}`;
            }
            return;
        }

        // Se tudo deu certo e veio JSON:
        const cliente = JSON.parse(respostaTexto);
        document.getElementById("resposta").innerText = JSON.stringify(cliente, null, 2);
    } catch (err) {
        document.getElementById("resposta").innerText = `Falha na requisição: ${err}`;
    }
});
