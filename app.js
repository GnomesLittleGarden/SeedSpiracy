// ===== helpers =====
const modal     = document.getElementById('email‑modal');
const openBtn   = document.getElementById('download‑btn');
const form      = document.getElementById('email‑form');

// open modal
openBtn.addEventListener('click', () => modal.classList.remove('hidden'));

// submit email → POST to the server
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value.trim();

  try {
    const res = await fetch('/download', {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ email })
    });

    if (res.ok) {
      // force a file download without re‑opening the modal
      const blob = await res.blob();
      const url  = window.URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = 'Seedspiracy_Field_Manual_v0.1.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      modal.classList.add('hidden');
      form.reset();
    } else {
      alert('Something went wrong. Try again?');
    }
  } catch (err) {
    console.error(err);
    alert('Network hiccup. Try once more.');
  }
});