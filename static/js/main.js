function initCharCounter(textareaId, counterId) {
    var textarea = document.getElementById(textareaId);
    var counter = document.getElementById(counterId);
    if (!textarea || !counter) return;

    function update() {
        var text = textarea.value.replace(/\s/g, '');
        counter.textContent = text.length;
        var hint = counter.parentElement.querySelector('.char-hint');
        if (hint) {
            if (text.length >= 800) {
                hint.textContent = '（字数达标）';
                hint.style.color = '#27ae60';
            } else if (text.length >= 600) {
                hint.textContent = '（建议再写 ' + (800 - text.length) + ' 字）';
                hint.style.color = '#f39c12';
            } else {
                hint.textContent = '（建议 800 字以上）';
                hint.style.color = '#e74c3c';
            }
        }
    }

    textarea.addEventListener('input', update);
    update();
}

function initSubmitLoading(formId, btnId) {
    var form = document.getElementById(formId);
    var btn = document.getElementById(btnId);
    if (!form || !btn) return;

    form.addEventListener('submit', function () {
        var text = btn.querySelector('.btn-text');
        var loading = btn.querySelector('.btn-loading');
        if (text && loading) {
            text.style.display = 'none';
            loading.style.display = 'inline';
            btn.disabled = true;
        }
    });
}

function clearForm() {
    document.getElementById('title').value = '';
    document.getElementById('essay').value = '';
    var counter = document.getElementById('char-count');
    if (counter) {
        counter.textContent = '0';
        var hint = counter.parentElement.querySelector('.char-hint');
        if (hint) {
            hint.textContent = '（建议 800 字以上）';
            hint.style.color = '#e74c3c';
        }
    }
}
