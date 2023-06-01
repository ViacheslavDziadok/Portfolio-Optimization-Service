document.addEventListener('DOMContentLoaded', function () {
    var selectDeselectBtn = document.getElementById('select-deselect-btn');
    var checkboxes = document.getElementsByName('companies[]');

    selectDeselectBtn.addEventListener('click', function () {
        var isChecked = false;

        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                isChecked = true;
                break;
            }
        }

        for (var j = 0; j < checkboxes.length; j++) {
            checkboxes[j].checked = !isChecked;
        }

        if (isChecked) {
            selectDeselectBtn.innerHTML = 'Select All';
        } else {
            selectDeselectBtn.innerHTML = 'Deselect All';
        }
    });
});