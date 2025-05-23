import ClassicEditor from "@ckeditor/ckeditor5-build-classic"

// Initialize rich text editor
document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("id_content")) {
    ClassicEditor.create(document.getElementById("id_content")).catch((error) => {
      console.error(error)
    })
  }
})
