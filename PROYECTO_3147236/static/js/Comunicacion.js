// Datos simulados
const courses = [
  {id: '601', name:'601 - A'},
  {id: '602', name:'602 - A'},
  {id: '603', name:'603 - A'},
  {id: '701', name:'701 - A'},
  {id: '702', name:'702 - A'},
  {id: '803', name:'803 - A'},
  {id: '901', name:'901 - A'},
  {id: '1001', name:'1001 - A'},
  {id: '1003', name:'1003 - A'},
];

const groupLinks = {
  '601': 'https://web.whatsapp.com/send?text=Grupo%20601',
  '602': 'https://web.whatsapp.com/send?text=Grupo%20602',
  '603': 'https://web.whatsapp.com/send?text=Grupo%20603',
  '701': 'https://web.whatsapp.com/send?text=Grupo%20701',
  '702': 'https://web.whatsapp.com/send?text=Grupo%20702',
  '803': 'https://web.whatsapp.com/send?text=Grupo%20803',
  '901': 'https://web.whatsapp.com/send?text=Grupo%20901',
  '1001': 'https://web.whatsapp.com/send?text=Grupo%201001',
  '1003': 'https://web.whatsapp.com/send?text=Grupo%201003'
};

const currentUser = {name: 'Profesor Ejemplo'};

// Elementos
const courseSelect = document.getElementById('courseSelect');
const coursesList = document.getElementById('coursesList');
const typeRow = document.getElementById('typeRow');
const fileBox = document.getElementById('fileBox');
const fileInput = document.getElementById('fileInput');
const fileNameEl = document.getElementById('fileName');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const feedback = document.getElementById('feedback');
const historyBody = document.getElementById('historyBody');

const confirmModal = document.getElementById('confirmModal');
const confirmText = document.getElementById('confirmText');
const cancelSend = document.getElementById('cancelSend');
const confirmSend = document.getElementById('confirmSend');

const successModal = document.getElementById('successModal');
const successText = document.getElementById('successText');
const closeSuccess = document.getElementById('closeSuccess');

// Estado
let selectedType = null;
let selectedFile = null;
let selectedCourseId = null;
let history = [];

// Inicialización
function init(){
  courses.forEach(c=>{
    const opt = document.createElement('option');
    opt.value = c.id; opt.textContent = c.name;
    courseSelect.appendChild(opt);

    const div = document.createElement('div');
    div.style.padding = '6px 8px'; div.style.cursor = 'pointer';
    div.textContent = c.name;
    div.addEventListener('click', ()=> {
      courseSelect.value = c.id;
      onCourseChange();
      window.scrollTo({top:0, behavior:'smooth'});
    });
    coursesList.appendChild(div);
  });

  typeRow.querySelectorAll('.btn-type').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      typeRow.querySelectorAll('.btn-type').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      selectedType = btn.dataset.type;
      updateControls();
    });
  });

  fileBox.addEventListener('click', ()=> fileInput.click());
  fileBox.addEventListener('keydown', (e)=>{ if(e.key==='Enter') fileInput.click(); });
  fileInput.addEventListener('change', onFileChosen);

  fileBox.addEventListener('dragover', e=>{ e.preventDefault(); fileBox.style.borderColor='#bbb'; });
  fileBox.addEventListener('dragleave', ()=> fileBox.style.borderColor='#ddd');
  fileBox.addEventListener('drop', e=>{
    e.preventDefault(); fileBox.style.borderColor='#ddd';
    if(e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });

  courseSelect.addEventListener('change', onCourseChange);

  sendBtn.addEventListener('click', onSendClick);
  clearBtn.addEventListener('click', clearForm);

  cancelSend.addEventListener('click', ()=> toggleModal(confirmModal,false));
  closeSuccess.addEventListener('click', ()=> toggleModal(successModal,false));
  confirmSend.addEventListener('click', doSend);

  loadHistory();
  renderHistory();
  updateControls();
}

function onCourseChange(){
  selectedCourseId = courseSelect.value || null;
  updateControls();
}

// Manejo de archivos
function onFileChosen(e){
  if(e.target.files && e.target.files[0]) handleFile(e.target.files[0]);
}
function handleFile(file){
  const allowed = [
    'application/pdf','application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg','image/png'
  ];
  const maxBytes = 8 * 1024 * 1024;
  if(!allowed.includes(file.type)){
    showFeedback('Tipo de archivo no permitido.', true);
    return;
  }
  if(file.size > maxBytes){
    showFeedback('Archivo muy grande. Máx 8MB.', true);
    return;
  }
  selectedFile = file;
  fileNameEl.textContent = `${file.name} · ${(file.size/1024/1024).toFixed(2)} MB`;
  showFeedback('', false);
  updateControls();
}

function updateControls(){
  sendBtn.disabled = !(selectedCourseId && selectedType && selectedFile);
}

function clearForm(){
  courseSelect.value = '';
  selectedCourseId = null;
  selectedType = null;
  selectedFile = null;
  fileInput.value = '';
  fileNameEl.textContent = '';
  typeRow.querySelectorAll('.btn-type').forEach(b=>b.classList.remove('active'));
  showFeedback('', false);
  updateControls();
}

// Feedback
function showFeedback(msg, isError){
  feedback.textContent = msg;
  feedback.style.color = isError ? 'var(--danger)' : '#333';
}

// Historial
function loadHistory(){
  try{
    const raw = localStorage.getItem('edu_envios_history_v1');
    history = raw ? JSON.parse(raw) : [];
  }catch(e){ history = []; }
}
function saveHistory(){
  localStorage.setItem('edu_envios_history_v1', JSON.stringify(history));
}
function addHistoryItem(item){
  history.unshift(item);
  if(history.length>60) history.pop();
  saveHistory();
  renderHistory();
}
function renderHistory(){
  historyBody.innerHTML = '';
  if(history.length===0){
    historyBody.innerHTML = `<tr><td colspan="6" style="color:#666;padding:10px">No hay envíos recientes</td></tr>`;
    return;
  }
  history.forEach(item=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${escapeHtml(item.fileName)}</td>
      <td>${escapeHtml(item.courseName)}</td>
      <td>${escapeHtml(item.type)}</td>
      <td>${escapeHtml(item.user)}</td>
      <td>${escapeHtml(new Date(item.date).toLocaleString())}</td>
      <td class="status ${item.status==='Enviado' ? 'sent' : 'err'}">${escapeHtml(item.status)}</td>`;
    historyBody.appendChild(tr);
  });
}

// Envío simulado
function onSendClick(){
  if(!selectedCourseId || !selectedType || !selectedFile) {
    showFeedback('Completa curso, tipo y archivo antes de enviar.', true);
    return;
  }
  const courseName = courses.find(c=>c.id===selectedCourseId)?.name || selectedCourseId;
  confirmText.textContent = `Vas a enviar "${selectedFile.name}" al curso ${courseName} como "${selectedType}". ¿Deseas continuar?`;
  toggleModal(confirmModal,true);
}
function toggleModal(modal, show){
  modal.style.display = show ? 'flex' : 'none';
  modal.setAttribute('aria-hidden', show ? 'false' : 'true');
}
function doSend(){
  toggleModal(confirmModal,false);
  const courseName = courses.find(c=>c.id===selectedCourseId)?.name || selectedCourseId;
  const fileName = selectedFile.name;
  const payload = {
    fileName, courseId:selectedCourseId, courseName, type:selectedType,
    user: currentUser.name, date: new Date().toISOString(), status:'Enviado'
  };
  addHistoryItem(payload);
  const text = encodeURIComponent(`[${courseName}] ${selectedType}\nArchivo: ${fileName}`);
  const url = groupLinks[selectedCourseId] || `https://web.whatsapp.com/send?text=${text}`;
  window.open(url, '_blank');
  successText.textContent = `Se intentó abrir WhatsApp para ${courseName}. Adjunta el archivo manualmente si es necesario.`;
  toggleModal(successModal,true);
  clearForm();
}

function escapeHtml(s){ return (s+'').replace(/[&<>"']/g, m=> ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

document.addEventListener('DOMContentLoaded', init);
