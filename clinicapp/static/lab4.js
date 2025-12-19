// ================= DOM READY =================
document.addEventListener("DOMContentLoaded", () => {
    // Patient
    window.patient_name = document.getElementById("patient_name");
    window.patient_age = document.getElementById("patient_age");
    window.patient_gender = document.getElementById("patient_gender");
    window.patient_phone = document.getElementById("patient_phone");
    window.patient_info = document.getElementById("patient_info");

    // Service
    window.service_name = document.getElementById("service_name");
    window.service_cost = document.getElementById("service_cost");
    window.drug_cost = document.getElementById("drug_cost");
    window.vat = document.getElementById("vat");
    window.total_payment = document.getElementById("total_payment");

    // Invoice
    window.invoice_body = document.getElementById("invoice_body");
    window.grand_total = document.getElementById("grand_total");

    // Modal
    window.saved_invoice_list = document.getElementById("saved_invoice_list");
    window.invoiceModal = document.getElementById("invoiceModal");
    window.detailModal = document.getElementById("detailModal");

    // Search & filter
    window.searchInput = document.getElementById("searchInput");
    window.filterDate = document.getElementById("filterDate");
    window.filterMonth = document.getElementById("filterMonth");
});

let editIndex = null;

// ================= CẬP NHẬT GIÁ =================
function updatePrice() {
    const price = parseInt(service_name.value) || 0;
    const drug = parseInt(drug_cost.value) || 0;
    const vatVal = (price + drug) * 0.1;
    const total = price + drug + vatVal;

    service_cost.value = price ? price.toLocaleString() + " VND" : "";
    vat.value = vatVal ? vatVal.toLocaleString() + " VND" : "";
    total_payment.value = total ? total.toLocaleString() + " VND" : "";
}

// ================= HIỂN THỊ BỆNH NHÂN =================
function showPatientInfo() {
    patient_info.innerHTML = `
        <p><strong>Họ tên:</strong> ${patient_name.value}</p>
        <p><strong>Tuổi:</strong> ${patient_age.value}</p>
        <p><strong>Giới tính:</strong> ${patient_gender.value}</p>
        <p><strong>SĐT:</strong> ${patient_phone.value}</p>
    `;
}

// ================= THÊM DỊCH VỤ =================
function addInvoiceRow() {
    if (!service_name.value) return alert("Vui lòng chọn dịch vụ");

    const row = document.createElement("tr");
    row.innerHTML = `
        <td></td>
        <td>${service_name.options[service_name.selectedIndex].text}</td>
        <td>${service_cost.value}</td>
        <td>${drug_cost.value ? Number(drug_cost.value).toLocaleString() + " VND" : "0 VND"}</td>
        <td>${vat.value}</td>
        <td>${total_payment.value}</td>
        <td>
            <button class="btn text-danger p-0" onclick="deleteRow(this)">
                <span class="material-symbols-rounded">delete</span>
            </button>
        </td>
    `;
    invoice_body.appendChild(row);
    updateRowNumbers();
}

// ================= XÓA DÒNG =================
function deleteRow(btn) {
    btn.closest("tr").remove();
    updateRowNumbers();
}

// ================= STT + TỔNG =================
function updateRowNumbers() {
    let sum = 0;
    document.querySelectorAll("#invoice_body tr").forEach((row, i) => {
        row.cells[0].textContent = i + 1;
        sum += parseInt(row.cells[5].textContent.replace(/\D/g, "")) || 0;
    });
    grand_total.innerHTML = `<strong>${sum.toLocaleString()} VND</strong>`;
}

// ================= LƯU HÓA ĐƠN =================
function saveInvoice() {
    const rows = document.querySelectorAll("#invoice_body tr");
    if (!rows.length) return alert("Chưa có dịch vụ");

    const invoice = {
        patient: {
            name: patient_name.value,
            age: patient_age.value,
            gender: patient_gender.value,
            phone: patient_phone.value
        },
        details: [...rows].map((r, i) => ({
            stt: i + 1,
            service: r.cells[1].textContent,
            serviceCost: r.cells[2].textContent,
            drugCost: r.cells[3].textContent,
            vat: r.cells[4].textContent,
            total: r.cells[5].textContent
        })),
        grandTotal: grand_total.innerText,
        createdAt: new Date().toLocaleString()
    };

    let invoices = JSON.parse(localStorage.getItem("invoices")) || [];

    if (editIndex !== null) {
        invoices[editIndex] = invoice;
        editIndex = null;
    } else {
        invoices.push(invoice);
    }

    localStorage.setItem("invoices", JSON.stringify(invoices));
    alert("Đã lưu hóa đơn");
    resetInvoiceForm();
}

// ================= RESET =================
function resetInvoiceForm() {
    patient_name.value = patient_age.value = patient_phone.value = "";
    patient_gender.selectedIndex = 0;
    patient_info.innerHTML = "<p>Chưa có thông tin bệnh nhân.</p>";

    service_name.selectedIndex = 0;
    service_cost.value = drug_cost.value = vat.value = total_payment.value = "";

    invoice_body.innerHTML = "";
    grand_total.innerHTML = "<strong>0 VND</strong>";
}

// ================= DANH SÁCH HÓA ĐƠN =================
function showSavedInvoices() {
    renderInvoices();
    new bootstrap.Modal(invoiceModal).show();
}

function renderInvoices() {
    const invoices = JSON.parse(localStorage.getItem("invoices")) || [];
    const search = searchInput.value.toLowerCase();
    const date = filterDate.value;
    const month = filterMonth.value;

    const list = invoices.filter(inv => {
        const textMatch =
            inv.patient.name.toLowerCase().includes(search) ||
            inv.patient.phone.includes(search);

        const d = new Date(inv.createdAt);
        const dateMatch = date ? d.toISOString().slice(0,10) === date : true;
        const monthMatch = month ? d.toISOString().slice(0,7) === month : true;

        return textMatch && dateMatch && monthMatch;
    });

    saved_invoice_list.innerHTML = list.length === 0
        ? "<p>Không có hóa đơn</p>"
        : list.map((inv, i) => `
            <div class="border rounded p-3 mb-3">
                <p><strong>Hóa đơn #${i + 1}</strong> (${inv.createdAt})</p>
                <p>${inv.patient.name} - ${inv.patient.phone}</p>
                <p><b>${inv.grandTotal}</b></p>

                <div class="d-flex gap-2">
                    <button class="btn btn-sm btn-info" onclick="viewInvoiceDetail(${i})">Chi tiết</button>
                    <button class="btn btn-sm btn-warning" onclick="editInvoice(${i})">Sửa</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteInvoice(${i})">Xóa</button>
                </div>
            </div>
        `).join("");
}

// ================= CHI TIẾT HÓA ĐƠN (ĐÃ SỬA) =================
function viewInvoiceDetail(index) {
    const invoices = JSON.parse(localStorage.getItem("invoices")) || [];
    const inv = invoices[index];
    if (!inv) return;

    const rows = inv.details.map(d => `
        <tr>
            <td>${d.service}</td>
            <td>${d.serviceCost}</td>
            <td>${d.drugCost}</td>
            <td>${d.vat}</td>
            <td>${d.total}</td>
        </tr>
    `).join("");

    document.getElementById("invoice_detail_content").innerHTML = `
        <p><strong>Họ tên:</strong> ${inv.patient.name}</p>
        <p><strong>SĐT:</strong> ${inv.patient.phone}</p>
        <p><strong>Ngày lập:</strong> ${inv.createdAt}</p>

        <table class="table table-bordered mt-3">
            <thead class="table-light">
                <tr>
                    <th>Dịch vụ</th>
                    <th>Chi phí</th>
                    <th>Thuốc</th>
                    <th>VAT</th>
                    <th>Tổng</th>
                </tr>
            </thead>
            <tbody>${rows}</tbody>
        </table>

        <div class="text-end fw-bold">
            Tổng thanh toán: ${inv.grandTotal}
        </div>
    `;

    new bootstrap.Modal(detailModal).show();
}

// ================= SỬA =================
function editInvoice(i) {
    const inv = JSON.parse(localStorage.getItem("invoices"))[i];
    editIndex = i;

    patient_name.value = inv.patient.name;
    patient_age.value = inv.patient.age;
    patient_gender.value = inv.patient.gender;
    patient_phone.value = inv.patient.phone;

    invoice_body.innerHTML = "";
    inv.details.forEach(d => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td></td>
            <td>${d.service}</td>
            <td>${d.serviceCost}</td>
            <td>${d.drugCost}</td>
            <td>${d.vat}</td>
            <td>${d.total}</td>
            <td></td>
        `;
        invoice_body.appendChild(row);
    });

    updateRowNumbers();
    bootstrap.Modal.getInstance(invoiceModal).hide();
}

// ================= XÓA =================
function deleteInvoice(i) {
    if (!confirm("Xóa hóa đơn này?")) return;
    const invoices = JSON.parse(localStorage.getItem("invoices"));
    invoices.splice(i, 1);
    localStorage.setItem("invoices", JSON.stringify(invoices));
    renderInvoices();
}
