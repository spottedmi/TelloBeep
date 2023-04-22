//SETTINGS BUTTON EVENTS/////

document.getElementById("uploadTokenBtn").onclick = function () {
    const body = JSON.stringify({
        token: document.getElementById("tokenInput").value,
      });

      fetch(`${window.location.origin}/token_list`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: body,
    });
};

document.getElementById("uploadFilterBtn").onclick = function () { 
      const body = JSON.stringify({
            word: document.getElementById("filterInput").value,
      });

      fetch(`${window.location.origin}/bad_words`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: body,
      });
};
