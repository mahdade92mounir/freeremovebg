window.onload = () => {
    feather?.replace();
}

Alpine?.store('viewer', {
    preview: null,
    result: null,
    loading: false,
    imageSize: "", // Ajout de la propriété imageSize
    fileChosen(event) {
        this.fileToDataUrl(event, src => {
            this.preview = src;
            this.result = null;
            this.updateImageSize(); // Appeler la fonction pour mettre à jour la taille de l'image
        })
    },
    fileToDataUrl(event, callback) {
        if (! event?.target?.files?.length) return

        let file = event.target.files[0],
            reader = new FileReader()

        reader.readAsDataURL(file)
        reader.onload = e => callback(e.target.result)
    },
    async removeBg() {
        if (this.isImageSizeValid()) {
            this.loading = true;
            this.processingTime = ""; // Réinitialiser le temps d'attente
            const startTime = new Date().getTime();
            const body = {
                "image": this.preview
            }
            try {
                const response = await axios.post("/removebg", body);
                this.result = response?.data?.result;
            } catch (error) {
                console.error(error);
            }
            const endTime = new Date().getTime();
            const totalTimeInSeconds = (endTime - startTime) / 1000;
            this.processingTime = `Temps d'attente estimé : ${totalTimeInSeconds.toFixed(2)} secondes`;

            // Vérifier si le traitement prend plus de 3 secondes
            if (totalTimeInSeconds > 3) {
                alert("Le traitement peut prendre un peu de temps. Veuillez patienter.");
            }

            this.loading = false;
        } else {
            alert("La taille de l'image doit être inférieure à 0.8 Mo.");
        }
    },
    async downloadImage() {
        const link = document.createElement('a');
        link.href = this.result;
        link.download = 'processed_image.png';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    },
    updateImageSize() { // Fonction pour mettre à jour la taille de l'image
        if (this.preview) {
            const imageSizeInBytes = this.preview.length; // Taille en octets
            const imageSizeInMB = (0.78*imageSizeInBytes / (1024 * 1024)).toFixed(2); // Convertit en Mo
            this.imageSize = `${imageSizeInMB} `;
        } else {
            this.imageSize = ""; // Réinitialise la taille si aucune image n'est sélectionnée
        }
    },
    isImageSizeValid() { // Fonction pour vérifier la taille de l'image
        if (this.preview) {
            const imageSizeInBytes = this.preview.length; // Taille en octets
            const imageSizeInMB = 0.78*imageSizeInBytes / (1024 * 1024); // Convertit en Mo
            return imageSizeInMB < 0.8; // Vérifie si la taille est inférieure à 1 Mo
        }
        return false; // Si aucune image n'est sélectionnée, la taille n'est pas valide
    }
});
