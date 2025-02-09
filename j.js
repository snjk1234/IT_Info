
// Initialize local storage
let data = JSON.parse(localStorage.getItem('crudData')) || [];

// Form elements
const Brance_nameInput = document.getElementById('Brance_name');
const DISPLAYInput = document.getElementById('DISPLAY');
const COMPUTERInput = document.getElementById('COMPUTER');
const MODELInput = document.getElementById('MODEL');
const GENARATIONInput = document.getElementById('GENARATION');
const HARDISKInput = document.getElementById('HARDISK');
const RAMInput = document.getElementById('RAM');
const PRINTERInput = document.getElementById('PRINTER');
const PRINTER_VERInput = document.getElementById('PRINTER_VER');
const addBtn = document.getElementById('addBtn');
const tbody = document.querySelector('#dataTable tbody');

// Render table
function renderTable() {
    tbody.innerHTML = '';
    data.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.Brance_name}</td>
            <td>${item.DISPLAY}</td>
            <td>${item.COMPUTER}</td>
            <td>${item.MODEL}</td>
            <td>${item.GENARATION}</td>
            <td>${item.HARDISK}</td>
            <td>${item.RAM}</td>
            <td>${item.PRINTER}</td>
            <td>${item.PRINTER_VER}</td>
            <td>
                <button class="action-btn edit-btn" onclick="editData(${index})">Edit</button>
                <button class="action-btn delete-btn" onclick="deleteData(${index})">Delete</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Add/Update data
addBtn.addEventListener('click', (e) => {
    e.preventDefault();
    
    if (!Brance_nameInput.value ||!DISPLAYInput.value ||!COMPUTERInput.value ||!MODELInput.value ||!GENARATIONInput.value ||!HARDISKInput.value || !RAMInput.value || !PRINTERInput.value || !PRINTER_VERInput.value) {
        alert('Please fill all fields!');
        return;
    }

    const newData = {
        Brance_name: Brance_nameInput.value,
        DISPLAY: DISPLAYInput.value,
        COMPUTER: COMPUTERInput.value,
        MODEL: MODELInput.value,
        GENARATION: GENARATIONInput.value,
        HARDISK: HARDISKInput.value,
        RAM: RAMInput.value,
        PRINTER: PRINTERInput.value,
        PRINTER_VER: PRINTER_VERInput.value,
    };

    if (addBtn.dataset.editIndex !== undefined) {
        // Update existing data
        data[addBtn.dataset.editIndex] = newData;
        addBtn.textContent = 'Add Data';
        delete addBtn.dataset.editIndex;
    } else {
        // Add new data
        data.push(newData);
    }

    localStorage.setItem('crudData', JSON.stringify(data));
    clearInputs();
    renderTable();
});

// Edit data
window.editData = (index) => {
    const item = data[index];
    Brance_nameInput.value = item.Brance_name;
    DISPLAYInput.value = item.DISPLAY;
    COMPUTERInput.value = item.COMPUTER;
    MODELInput.value = item.MODEL;
    GENARATIONInput.value = item.GENARATION;
    HARDISKInput.value = item.HARDISK;
    RAMInput.value = item.RAM;
    PRINTERInput.value = item.PRINTER;
    PRINTER_VERInput.value = item.PRINTER_VER;
    
    addBtn.textContent = 'Update Data';
    addBtn.dataset.editIndex = index;
};

// Delete data
window.deleteData = (index) => {
    if (confirm('Are you sure you want to delete this record?')) {
        data.splice(index, 1);
        localStorage.setItem('crudData', JSON.stringify(data));
        renderTable();
    }
};

// Clear inputs
function clearInputs() {
    Brance_nameInput.value = '';
    DISPLAYInput.value = '';
    COMPUTERInput.value = '';
    MODELInput.value = '';
    GENARATIONInput.value = '';
    HARDISKInput.value = '';
    RAMInput.value = '';
    PRINTERInput.value = '';
    PRINTER_VERInput.value = '';
}
// Initial render
renderTable();
window.addEventListener('DOMContentLoaded', renderTable);
