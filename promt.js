document.getElementById("upload-button").addEventListener("click", () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '*/*'; // Aceita todos os tipos de arquivos
  
    input.addEventListener('change', async () => {
      const file = input.files[0];
      if (!file) return alert("Nenhum arquivo selecionado!");
  
      const formData = new FormData();
      formData.append('file', file);
  
      try {
        const response = await fetch('/upload', {
          method: 'POST',
          body: formData,
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          alert(`Erro: ${errorData.error}`);
          return;
        }
  
        const data = await response.json();
        alert(`Upload bem-sucedido! Link: ${data.file_url}`);
        // Exibe o link no DOM
        const link = document.createElement('a');
        link.href = data.file_url;
        link.textContent = "Clique aqui para acessar o arquivo";
        link.target = "_blank";
        document.body.appendChild(link);
      } catch (error) {
        console.error('Erro no upload:', error);
        alert("Erro no upload. Tente novamente.");
      }
    });
  
    input.click();
  });
  