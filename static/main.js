function handleClick(button) { 
    /*  
    This function handles the click event for the "View Gallery" button.
    It toggles the display of a gallery row containing images related to the product.
    If the gallery is already displayed, it removes it and changes the button text back to "View Gallery".

    Args:
        button: The button element that was clicked.
    */


    // Get the array of image URLs from the button's data attribute
    const images = JSON.parse(button.dataset.images); 
    const productRow = button.closest(".product-row");

    // Check if the next row is already a gallery row, and if so, remove it and change the button text back to "View Gallery"
    const nextRow = productRow.nextElementSibling;
    if (nextRow?.classList.contains("gallery-row")) {
        nextRow.remove();
        button.textContent = "View Gallery";
        return;
    }

    // Create a new row for the gallery and populate it with images
    // Structure: galleryRow (tr) -> galleryCell (td) -> galleryDiv (div) -> images
    const galleryRow = document.createElement("tr");
    galleryRow.classList.add("gallery-row");

    const galleryCell = document.createElement("td");
    galleryCell.colSpan = productRow.children.length;

    const galleryDiv = document.createElement("div");       
    galleryDiv.classList.add("gallery-container");

    images.forEach((imageUrl) => {
        const image = document.createElement("img");

        image.src = imageUrl;
        image.alt = "Product image";
        image.width = 150;

        galleryDiv.appendChild(image);
    });

    galleryCell.appendChild(galleryDiv);
    galleryRow.appendChild(galleryCell);

    productRow.insertAdjacentElement("afterend", galleryRow);
    button.textContent = "Close Gallery";
}