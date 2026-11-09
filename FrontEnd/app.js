'use strict';
const API = (window.TASKFLOW_API_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
const $ = (id) => document.getElementById(id);
const state = { token: sessionStorage.getItem('taskflow_token'), user: null, tasks: [], filter: 'all', search: '', sort: 'new', editingId: null, registering: false };
let toastTimer;
function toast(message, error = false) { const el = $('toast'); el.textContent = message; el.className = `toast show${error ? ' error' : ''}`; clearTimeout(toastTimer); toastTimer = setTimeout(() => el.className = 'toast', 3500); }
async function request(path, options = {}) {
  const headers = { ...(options.body ? { 'Content-Type': 'application/json' } : {}), ...(state.token ? { Authorization: `Bearer ${state.token}` } : {}), ...options.headers };
  let response;
  try { response = await fetch(`${API}${path}`, { ...options, headers }); }
  catch { throw new Error('Não foi possível conectar à API. Verifique se o FastAPI está rodando e se o CORS foi configurado.'); }
  const raw = await response.text(); let data; try { data = raw ? JSON.parse(raw) : null; } catch { data = raw; }
  if (!response.ok) {
    if (response.status === 401 && !path.includes('/auth/login')) logout(false);
    let detail = data?.detail || data?.message || `Erro HTTP ${response.status}`;
    if (Array.isArray(detail)) detail = detail.map(x => x.msg || 'Dados inválidos').join('; ');
    throw new Error(typeof detail === 'string' ? detail : 'Não foi possível concluir a operação.');
  }
  return data;
}
function showAuth() { $('authView').classList.remove('hidden'); $('appView').classList.add('hidden'); }
function showApp() { $('authView').classList.add('hidden'); $('appView').classList.remove('hidden'); }
function logout(notify = true) { state.token = null; state.user = null; state.tasks = []; sessionStorage.removeItem('taskflow_token'); showAuth(); if (notify) toast('Você saiu da sua conta.'); }
function setRegisterMode(enabled) { state.registering = enabled; $('nameField').classList.toggle('hidden', !enabled); $('name').required = enabled; $('authTitle').textContent = enabled ? 'Crie sua conta' : 'Bem-vindo de volta'; $('authSubtitle').textContent = enabled ? 'Comece a organizar seus dias com mais leveza.' : 'Entre na sua conta para continuar de onde parou.'; $('authSubmit').innerHTML = enabled ? 'Criar minha conta <span>→</span>' : 'Entrar na minha conta <span>→</span>'; $('authSwitchText').textContent = enabled ? 'Já tem uma conta?' : 'Ainda não tem uma conta?'; $('authSwitch').textContent = enabled ? 'Entrar' : 'Criar conta'; $('password').autocomplete = enabled ? 'new-password' : 'current-password'; }
async function login(email, senha) { const data = await request('/auth/login', { method: 'POST', body: JSON.stringify({ email, senha }) }); if (!data?.access_token) throw new Error('A API não retornou um token de acesso.'); state.token = data.access_token; sessionStorage.setItem('taskflow_token', state.token); await loadUser(); await loadTasks(); showApp(); toast('Bem-vindo ao seu espaço!'); }
async function loadUser() { const user = await request('/auth/me'); state.user = user; const first = (user.nome || 'usuário').trim().split(/\s+/)[0]; $('greetingName').textContent = first; $('sideName').textContent = user.nome || 'Usuário'; $('sideEmail').textContent = user.email || ''; const initial = first.charAt(0).toUpperCase(); $('sideAvatar').textContent = initial; $('topAvatar').textContent = initial; }
async function loadTasks() { const tasks = await request('/tarefas/minhas'); if (!Array.isArray(tasks)) throw new Error('A API retornou um formato inesperado para as tarefas.'); state.tasks = tasks; render(); }
function render() { const total = state.tasks.length, done = state.tasks.filter(t => t.concluida).length, pending = total - done; $('statTotal').textContent = total; $('statPending').textContent = pending; $('statDone').textContent = done; const percent = total ? Math.round(done / total * 100) : 0; $('statPercent').textContent = `${percent}%`; $('progressFill').style.width = `${percent}%`; $('taskCount').textContent = total;
  document.querySelectorAll('[data-filter]').forEach(btn => btn.classList.toggle('active', btn.dataset.filter === state.filter));
  let tasks = state.tasks.filter(t => state.filter === 'all' || (state.filter === 'done' ? t.concluida : !t.concluida));
  const query = state.search.trim().toLocaleLowerCase('pt-BR'); if (query) tasks = tasks.filter(t => `${t.titulo || ''} ${t.descricao || ''}`.toLocaleLowerCase('pt-BR').includes(query));
  tasks = [...tasks].sort((a,b) => state.sort === 'az' ? String(a.titulo).localeCompare(String(b.titulo), 'pt-BR') : state.sort === 'old' ? Number(a.id)-Number(b.id) : Number(b.id)-Number(a.id));
  $('tasksList').replaceChildren(); $('emptyState').classList.toggle('hidden', tasks.length !== 0);
  $('emptyMessage').textContent = total === 0 ? 'Crie sua primeira tarefa e comece a organizar suas ideias.' : 'Nenhuma tarefa corresponde aos filtros selecionados.';
  for (const task of tasks) $('tasksList').appendChild(taskElement(task));
}
function taskElement(task) { const row = document.createElement('article'); row.className = `task-row${task.concluida ? ' is-done' : ''}`;
  const checkbox = document.createElement('input'); checkbox.type = 'checkbox'; checkbox.className = 'task-check'; checkbox.checked = Boolean(task.concluida); checkbox.setAttribute('aria-label', `Marcar ${task.titulo} como ${task.concluida ? 'pendente' : 'concluída'}`); checkbox.addEventListener('change', async () => { checkbox.disabled = true; try { await updateTask(task.id, { titulo: task.titulo, descricao: task.descricao || '', concluida: checkbox.checked }); toast('Status atualizado!'); } catch (e) { checkbox.checked = !checkbox.checked; toast(e.message, true); } finally { checkbox.disabled = false; } });
  const info = document.createElement('div'); info.className = 'task-info'; const title = document.createElement('strong'); title.textContent = task.titulo || 'Sem título'; const description = document.createElement('p'); description.textContent = task.descricao || 'Sem descrição'; info.append(title, description);
  const status = document.createElement('span'); status.className = `status${task.concluida ? ' done' : ''}`; status.textContent = task.concluida ? 'Concluída' : 'Pendente';
  const actions = document.createElement('div'); actions.className = 'row-actions'; const edit = document.createElement('button'); edit.textContent = '✎'; edit.title = 'Editar tarefa'; edit.setAttribute('aria-label', `Editar ${task.titulo}`); edit.addEventListener('click', () => openModal(task)); const del = document.createElement('button'); del.textContent = '♲'; del.title = 'Excluir tarefa'; del.className = 'danger'; del.setAttribute('aria-label', `Excluir ${task.titulo}`); del.addEventListener('click', () => deleteTask(task)); actions.append(edit,del); row.append(checkbox,info,status,actions); return row; }
async function updateTask(id, data) { await request(`/tarefas/atualizar/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(data) }); await loadTasks(); }
async function deleteTask(task) { if (!window.confirm(`Excluir a tarefa "${task.titulo}"? Esta ação não pode ser desfeita.`)) return; try { await request(`/tarefas/deletar/${encodeURIComponent(task.id)}`, { method: 'DELETE' }); await loadTasks(); toast('Tarefa excluída.'); } catch (e) { toast(e.message, true); } }
function openModal(task = null) { state.editingId = task ? task.id : null; $('modalTitle').textContent = task ? 'Editar tarefa' : 'Nova tarefa'; $('taskTitle').value = task?.titulo || ''; $('taskDescription').value = task?.descricao || ''; $('taskDone').checked = Boolean(task?.concluida); $('modalBackdrop').classList.remove('hidden'); $('taskTitle').focus(); }
function closeModal() { $('modalBackdrop').classList.add('hidden'); state.editingId = null; }
$('authSwitch').addEventListener('click', () => setRegisterMode(!state.registering));
$('authForm').addEventListener('submit', async e => { e.preventDefault(); const button = $('authSubmit'); button.disabled = true; const email = $('email').value.trim(), senha = $('password').value; try { if (state.registering) { await request('/usuarios/cadastrar', { method: 'POST', body: JSON.stringify({ nome: $('name').value.trim(), email, senha }) }); setRegisterMode(false); toast('Conta criada! Agora faça login.'); } else await login(email, senha); } catch (err) { toast(err.message, true); } finally { button.disabled = false; } });
$('logoutBtn').addEventListener('click', () => logout()); $('newTaskBtn').addEventListener('click', () => openModal()); $('emptyAddBtn').addEventListener('click', () => openModal()); $('closeModal').addEventListener('click', closeModal); $('cancelModal').addEventListener('click', closeModal); $('modalBackdrop').addEventListener('click', e => { if (e.target === $('modalBackdrop')) closeModal(); }); document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
$('taskForm').addEventListener('submit', async e => { e.preventDefault(); const btn = $('saveTaskBtn'); btn.disabled = true; const data = { titulo: $('taskTitle').value.trim(), descricao: $('taskDescription').value.trim(), concluida: $('taskDone').checked }; if (!data.titulo) { toast('Informe o título da tarefa.', true); btn.disabled = false; return; } try { if (state.editingId !== null) { await updateTask(state.editingId, data); toast('Tarefa atualizada!'); } else { await request('/tarefas/criar', { method: 'POST', body: JSON.stringify(data) }); await loadTasks(); toast('Tarefa criada!'); } closeModal(); } catch (err) { toast(err.message, true); } finally { btn.disabled = false; } });
document.querySelectorAll('[data-filter]').forEach(btn => btn.addEventListener('click', () => { state.filter = btn.dataset.filter; render(); })); $('searchInput').addEventListener('input', e => { state.search = e.target.value; render(); }); $('sortSelect').addEventListener('change', e => { state.sort = e.target.value; render(); });
$('todayLabel').textContent = new Intl.DateTimeFormat('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' }).format(new Date());
(async () => { if (!state.token) return showAuth(); try { await loadUser(); await loadTasks(); showApp(); } catch (err) { logout(false); toast(err.message, true); } })();
