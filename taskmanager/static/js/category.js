// Used to handle the An invalid form control is not focusable Error
document.querySelector("form").addEventListener('submit', function(e){
    e.preventDefault();

    if(!this.category_id.value){
        console.log("No category has been chosen");
        return;
    } else {
        this.submit();
    }
})