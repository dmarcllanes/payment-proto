from fasthtml.common import (
    Body, Button, Div, Form, H1, Head, Html,
    Input, Label, Link, Main, Meta, P, Script, Span, Style, Title,
)

STYLE = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { height: 100%; }

body {
  background: #060a12;
  color: #e2e8f0;
  font-family: 'Inter', system-ui, sans-serif;
  min-height: 100svh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-x: hidden;
  overflow-y: auto;
  padding: max(1.5rem, env(safe-area-inset-top)) 0 max(1.5rem, env(safe-area-inset-bottom));
}

/* Dot grid */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(rgba(0,168,150,0.07) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
  z-index: 0;
}

/* Animated orbs */
.orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  z-index: 0;
}
.orb-1 { width:500px;height:500px;background:rgba(0,168,150,0.13);top:-160px;left:-160px;animation:drift1 14s ease-in-out infinite; }
.orb-2 { width:360px;height:360px;background:rgba(0,168,150,0.08);bottom:-100px;right:-80px;animation:drift2 18s ease-in-out infinite; }
.orb-3 { width:260px;height:260px;background:rgba(0,220,200,0.06);top:40%;left:55%;animation:drift3 11s ease-in-out infinite; }
@keyframes drift1 { 0%,100%{transform:translate(0,0)scale(1)} 33%{transform:translate(70px,50px)scale(1.12)} 66%{transform:translate(-30px,80px)scale(0.94)} }
@keyframes drift2 { 0%,100%{transform:translate(0,0)scale(1)} 50%{transform:translate(-70px,-50px)scale(1.1)} }
@keyframes drift3 { 0%,100%{transform:translate(-50%,-50%)scale(1)} 50%{transform:translate(-50%,-50%)scale(1.25)} }

/* Page entry */
.page-wrap {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 460px;
  padding: 0 1.25rem 2rem;
  animation: page-entry 0.65s cubic-bezier(0.34,1.1,0.64,1) both;
}
@keyframes page-entry {
  from { opacity:0; transform:translateY(28px); }
  to   { opacity:1; transform:translateY(0); }
}

/* ── 3D Card ── */
.card-scene { perspective:1200px; height:212px; margin-bottom:1.75rem; }
.card-3d {
  width:100%;height:100%;position:relative;
  transform-style:preserve-3d;
  transition:transform 0.65s cubic-bezier(0.4,0,0.2,1);
}
.card-3d.flipped { transform:rotateY(180deg); }

.card-face {
  position:absolute;inset:0;border-radius:20px;padding:22px 26px;
  backface-visibility:hidden;-webkit-backface-visibility:hidden;
  overflow:hidden;display:flex;flex-direction:column;
}
.card-front {
  background:linear-gradient(135deg,#00BFA5 0%,#00796B 55%,#004D40 100%);
  box-shadow:0 24px 60px rgba(0,168,150,0.42),0 8px 24px rgba(0,0,0,0.5);
}
.card-front::before {
  content:'';position:absolute;width:290px;height:290px;background:rgba(255,255,255,0.07);
  border-radius:50%;top:-110px;right:-65px;
}
.card-front::after {
  content:'';position:absolute;width:190px;height:190px;background:rgba(255,255,255,0.05);
  border-radius:50%;bottom:-75px;left:-45px;
}
.card-back {
  background:linear-gradient(150deg,#004D40 0%,#00695C 100%);
  box-shadow:0 24px 60px rgba(0,100,90,0.3),0 8px 24px rgba(0,0,0,0.5);
  transform:rotateY(180deg);
}

.card-top-row { display:flex;justify-content:space-between;align-items:flex-start; }
.card-chip {
  width:42px;height:32px;
  background:linear-gradient(135deg,#FFD54F,#F9A825);
  border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.3);
  position:relative;flex-shrink:0;
}
.card-chip::before { content:'';position:absolute;inset:5px 4px;border:1.5px solid rgba(0,0,0,0.18);border-radius:3px; }
.card-chip::after  { content:'';position:absolute;width:1.5px;top:5px;bottom:5px;left:50%;background:rgba(0,0,0,0.15); }

.card-contactless {
  font-size:1.15rem;color:rgba(255,255,255,0.6);
  margin-right:0.3rem;margin-top:0.1rem;
}
.card-logo { font-size:1rem;font-weight:900;color:rgba(255,255,255,0.88);letter-spacing:0.12em; }
.card-logo-wrap { display:flex;flex-direction:column;align-items:flex-end;gap:0.1rem; }

.card-number-preview {
  font-size:1.28rem;letter-spacing:0.22em;
  font-family:'Courier New',monospace;color:#fff;
  margin:auto 0 18px;text-shadow:0 1px 6px rgba(0,0,0,0.25);
}
.card-bottom-row { display:flex;justify-content:space-between;align-items:flex-end; }
.card-field-label { font-size:0.57rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.5);margin-bottom:2px; }
.card-field-value { font-size:0.82rem;font-weight:600;color:#fff;letter-spacing:0.05em;max-width:160px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap; }

.card-stripe { height:42px;background:rgba(0,0,0,0.55);margin:14px -26px 16px; }
.cvv-strip { background:rgba(255,255,255,0.92);border-radius:5px;height:34px;display:flex;align-items:center;justify-content:flex-end;padding:0 14px;margin-bottom:auto; }
.cvv-dots { font-family:'Courier New',monospace;font-size:1rem;color:#1a1a1a;letter-spacing:0.14em; }
.card-back-footer { font-size:0.63rem;color:rgba(255,255,255,0.38);text-align:right;margin-top:auto; }

/* ── Glass card ── */
.glass-wrap { position:relative; }
.glass-wrap::before {
  content:'';position:absolute;inset:-1px;
  border-radius:1.6rem;
  background:linear-gradient(135deg,rgba(0,191,165,0.35) 0%,rgba(0,191,165,0.05) 50%,rgba(0,191,165,0.2) 100%);
  z-index:-1;
  animation:border-glow 4s ease-in-out infinite alternate;
}
@keyframes border-glow {
  from { opacity:0.5; }
  to   { opacity:1; }
}

.glass {
  background:rgba(255,255,255,0.03);
  border:1px solid transparent;
  backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);
  border-radius:1.5rem;padding:1.75rem;
  box-shadow:0 16px 60px rgba(0,0,0,0.55),inset 0 1px 0 rgba(255,255,255,0.06);
}

.header { margin-bottom:1.4rem; }
.badge {
  display:inline-flex;align-items:center;gap:0.45rem;
  background:rgba(0,168,150,0.15);color:#00BFA5;
  border:1px solid rgba(0,168,150,0.3);border-radius:9999px;
  padding:0.2rem 0.75rem;font-size:0.68rem;font-weight:700;
  letter-spacing:0.07em;text-transform:uppercase;margin-bottom:0.65rem;
}
.badge-dot {
  width:6px;height:6px;background:#00BFA5;border-radius:50%;flex-shrink:0;
  animation:pulse-dot 2.5s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%,100%{opacity:1;box-shadow:0 0 4px #00BFA5}
  50%{opacity:0.4;box-shadow:0 0 14px #00BFA5,0 0 28px rgba(0,191,165,0.35)}
}
h1 { font-size:1.5rem;font-weight:800;line-height:1.2;margin-bottom:0.25rem;color:#ffffff; }
.subtitle { font-size:0.78rem;color:#94a3b8;letter-spacing:0.04em; }

/* Form sections */
.section-label {
  font-size:0.65rem;text-transform:uppercase;letter-spacing:0.12em;
  color:#94a3b8;font-weight:700;margin:1rem 0 0.65rem;
  display:flex;align-items:center;gap:0.6rem;
}
.section-label::after { content:'';flex:1;height:1px;background:rgba(255,255,255,0.1); }

.row { display:flex;gap:0.6rem; }
.row .field { flex:1;min-width:0; }
.field { margin-bottom:0.85rem; }
.field label { display:block;font-size:0.72rem;color:#cbd5e1;margin-bottom:0.4rem;letter-spacing:0.06em;text-transform:uppercase;font-weight:600;transition:color 0.2s; }
.field:focus-within label { color:#00BFA5; }
.field input {
  width:100%;background:rgba(255,255,255,0.07);
  border:1px solid rgba(255,255,255,0.12);border-radius:0.65rem;
  padding:0.75rem 0.9rem;color:#ffffff;font-size:1rem;outline:none;
  transition:border-color 0.2s,box-shadow 0.2s,background 0.2s;
  -webkit-appearance:none;appearance:none;
}
.field input::placeholder { color:#64748b; }
.field input:focus { border-color:rgba(0,191,165,0.65);background:rgba(0,168,150,0.07);box-shadow:0 0 0 3px rgba(0,168,150,0.14),0 0 20px rgba(0,168,150,0.05); }

/* Button */
.jade-btn {
  position:relative;width:100%;padding:0.9rem;margin-top:0.6rem;
  border:none;border-radius:0.85rem;
  background:linear-gradient(135deg,#00BFA5 0%,#00796B 100%);
  color:#fff;font-weight:700;font-size:0.97rem;cursor:pointer;
  overflow:hidden;transition:transform 0.15s ease,box-shadow 0.2s ease;
  box-shadow:0 4px 24px rgba(0,168,150,0.38);letter-spacing:0.04em;
}
.jade-btn::after {
  content:'';position:absolute;top:0;left:-100%;width:55%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);
  transform:skewX(-22deg);transition:left 0.55s ease;
}
.jade-btn:hover::after { left:160%; }
.jade-btn:hover:not(:disabled) { transform:translateY(-2px);box-shadow:0 10px 36px rgba(0,168,150,0.52); }
.jade-btn:active:not(:disabled) { transform:translateY(0);box-shadow:0 4px 20px rgba(0,168,150,0.35); }
.jade-btn:disabled { opacity:0.65;cursor:not-allowed; }
.btn-inner { display:flex;align-items:center;justify-content:center;gap:0.5rem; }
.spinner { display:none;width:17px;height:17px;border:2.5px solid rgba(255,255,255,0.3);border-top-color:#fff;border-radius:50%;animation:spin 0.65s linear infinite;flex-shrink:0; }
@keyframes spin { to{transform:rotate(360deg)} }

/* Security bar */
.security-bar {
  display:flex;align-items:center;justify-content:center;gap:1rem;
  margin-top:1.25rem;padding-top:1rem;
  border-top:1px solid rgba(255,255,255,0.08);
  font-size:0.7rem;color:#64748b;letter-spacing:0.04em;
}
.security-item { display:flex;align-items:center;gap:0.3rem; }
.security-dot { width:4px;height:4px;border-radius:50%;background:#334155; }

/* ── Confirm Modal ── */
.confirm-overlay {
  position:fixed;inset:0;z-index:8888;
  display:flex;align-items:center;justify-content:center;
  background:rgba(6,10,18,0.85);
  backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
  animation:overlay-in 0.25s ease both;
  padding:1.5rem;
}
.confirm-card {
  background:rgba(15,22,36,0.98);
  border:1px solid rgba(0,168,150,0.25);
  border-radius:1.5rem;padding:2rem;
  width:100%;max-width:360px;
  box-shadow:0 24px 60px rgba(0,0,0,0.6),inset 0 1px 0 rgba(255,255,255,0.06);
  animation:content-pop 0.3s cubic-bezier(0.34,1.4,0.64,1) both;
}
.confirm-icon {
  width:56px;height:56px;border-radius:50%;
  background:linear-gradient(135deg,rgba(0,191,165,0.2),rgba(0,121,107,0.2));
  border:1px solid rgba(0,191,165,0.3);
  display:flex;align-items:center;justify-content:center;
  font-size:1.5rem;margin:0 auto 1.2rem;
}
.confirm-title { font-size:1.15rem;font-weight:700;color:#f1f5f9;text-align:center;margin-bottom:0.3rem; }
.confirm-sub { font-size:0.78rem;color:#64748b;text-align:center;margin-bottom:1.5rem; }
.confirm-row {
  display:flex;justify-content:space-between;align-items:center;
  padding:0.65rem 0;border-bottom:1px solid rgba(255,255,255,0.05);
  font-size:0.82rem;
}
.confirm-row:last-of-type { border-bottom:none;margin-bottom:1.25rem; }
.confirm-key { color:#64748b; }
.confirm-val { color:#e2e8f0;font-weight:600; }
.confirm-amount { color:#00BFA5;font-size:1.1rem;font-weight:800; }
.confirm-actions { display:flex;gap:0.6rem;margin-top:0.5rem; }
.btn-cancel {
  flex:1;padding:0.78rem;border-radius:0.75rem;
  background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
  color:#94a3b8;font-weight:600;font-size:0.9rem;cursor:pointer;
  transition:all 0.2s;
}
.btn-cancel:hover { background:rgba(255,255,255,0.09);color:#e2e8f0; }
.btn-confirm {
  flex:2;padding:0.78rem;border-radius:0.75rem;
  background:linear-gradient(135deg,#00BFA5,#00796B);
  border:none;color:#fff;font-weight:700;font-size:0.9rem;cursor:pointer;
  transition:transform 0.15s,box-shadow 0.2s;
  box-shadow:0 4px 20px rgba(0,168,150,0.35);
}
.btn-confirm:hover { transform:translateY(-1px);box-shadow:0 8px 28px rgba(0,168,150,0.5); }

/* Result */
.result-card { margin-top:1rem;padding:0.9rem 1rem;border-radius:0.75rem;animation:slide-up 0.3s ease; }
@keyframes slide-up { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.result-success { background:rgba(0,168,150,0.1);border:1px solid rgba(0,168,150,0.3); }
.result-error   { background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.3); }

/* ── Success Overlay ── */
.success-overlay {
  position:fixed;inset:0;z-index:9999;
  display:flex;align-items:center;justify-content:center;
  background:rgba(6,10,18,0.94);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  animation:overlay-in 0.4s ease both;cursor:pointer;
}
@keyframes overlay-in { from{opacity:0} to{opacity:1} }

.burst-ring {
  position:absolute;width:320px;height:320px;border-radius:50%;
  border:1.5px solid rgba(0,191,165,0.4);
  animation:burst-expand 1.4s ease-out both;pointer-events:none;
}
.burst-ring-2 { animation-delay:0.3s;border-color:rgba(0,191,165,0.18);width:480px;height:480px; }
@keyframes burst-expand { from{transform:scale(0);opacity:1} to{transform:scale(1);opacity:0} }

.success-content {
  position:relative;z-index:1;text-align:center;padding:2rem;
  animation:content-pop 0.55s cubic-bezier(0.34,1.56,0.64,1) 0.15s both;cursor:default;
}
@keyframes content-pop { from{transform:scale(0.7);opacity:0} to{transform:scale(1);opacity:1} }

.check-circle {
  width:96px;height:96px;border-radius:50%;
  background:linear-gradient(135deg,#00BFA5,#00796B);
  display:flex;align-items:center;justify-content:center;
  margin:0 auto 1.5rem;
  box-shadow:0 0 0 0 rgba(0,191,165,0.5),0 20px 50px rgba(0,168,150,0.4);
  animation:ring-pulse 1.5s ease-out 0.6s 3;
}
@keyframes ring-pulse {
  0%  {box-shadow:0 0 0 0 rgba(0,191,165,0.5),0 20px 50px rgba(0,168,150,0.4)}
  70% {box-shadow:0 0 0 28px rgba(0,191,165,0),0 20px 50px rgba(0,168,150,0.4)}
  100%{box-shadow:0 0 0 0 rgba(0,191,165,0),0 20px 50px rgba(0,168,150,0.4)}
}
.check-path {
  stroke-dasharray: 70;
  stroke-dashoffset: 70;
  animation: draw-check 0.5s cubic-bezier(0.4,0,0.2,1) 0.55s forwards;
}
@keyframes draw-check { to { stroke-dashoffset: 0; } }

.success-amount { font-size:2.4rem;font-weight:900;color:#fff;margin-bottom:0.4rem;letter-spacing:-0.02em; }
.success-title {
  font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;
  background:linear-gradient(135deg,#00BFA5,#4dd0c4);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.success-id { font-size:0.7rem;color:#334155;font-family:monospace;margin-bottom:1.75rem; }

.dismiss-btn {
  background:linear-gradient(135deg,#00BFA5,#00796B);color:#fff;
  font-weight:700;font-size:0.95rem;border:none;border-radius:9999px;
  padding:0.78rem 2.2rem;cursor:pointer;letter-spacing:0.04em;
  transition:transform 0.15s,box-shadow 0.2s;
  box-shadow:0 4px 20px rgba(0,168,150,0.4);
}
.dismiss-btn:hover { transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,168,150,0.55); }

/* ── Responsive ── */
@media (max-width:360px) {
  .page-wrap{padding:0 0.75rem 1.5rem}
  .card-scene{height:165px;margin-bottom:1.1rem}
  .card-face{padding:16px 18px}
  .card-number-preview{font-size:1rem;letter-spacing:0.14em}
  .glass{padding:1.1rem;border-radius:1.1rem}
  h1{font-size:1.2rem}
  .row{gap:0.45rem}
}
@media (max-height:600px) and (orientation:landscape) {
  body{align-items:flex-start}
  .card-scene{height:150px;margin-bottom:0.9rem}
  .badge{display:none}
}
@media (min-width:540px) { .page-wrap{max-width:500px} .glass{padding:2rem} }
@media (hover:none) and (pointer:coarse) {
  .field input{padding:0.8rem 0.9rem;min-height:48px}
  .jade-btn{padding:1rem;min-height:52px}
}
"""

SCRIPT = """
Xendit.setPublishableKey(window._xenditPK);

function updatePreview() {
  var num = document.getElementById("card-number").value.replace(/\\s/g,"");
  var padded = (num+"••••••••••••••••").slice(0,16);
  document.getElementById("preview-number").textContent = padded.match(/.{1,4}/g).join("  ");
  var fn = document.getElementById("first-name").value.trim();
  var ln = document.getElementById("last-name").value.trim();
  document.getElementById("preview-name").textContent = [fn,ln].filter(Boolean).join(" ").toUpperCase()||"FULL NAME";
  var m = document.getElementById("exp-month").value.trim().padStart(2,"0")||"MM";
  var y = document.getElementById("exp-year").value.trim().slice(-2)||"YY";
  document.getElementById("preview-expiry").textContent = m+"/"+y;
  var cvv = document.getElementById("cvn").value;
  document.getElementById("preview-cvv").textContent = cvv?"•".repeat(Math.min(cvv.length,4)):"•••";
}

document.getElementById("card-number").addEventListener("input",function(e){
  var v=e.target.value.replace(/\\D/g,"").slice(0,16);
  e.target.value=v.match(/.{1,4}/g)?v.match(/.{1,4}/g).join(" "):v;
  updatePreview();
});
document.getElementById("exp-month").addEventListener("input",function(e){e.target.value=e.target.value.replace(/\\D/g,"").slice(0,2);updatePreview();});
document.getElementById("exp-year").addEventListener("input",function(e){e.target.value=e.target.value.replace(/\\D/g,"").slice(0,4);updatePreview();});
document.getElementById("cvn").addEventListener("input",function(e){e.target.value=e.target.value.replace(/\\D/g,"").slice(0,4);updatePreview();});
["first-name","last-name"].forEach(function(id){document.getElementById(id).addEventListener("input",updatePreview);});

document.getElementById("cvn").addEventListener("focus",function(){document.getElementById("card-3d").classList.add("flipped");});
document.getElementById("cvn").addEventListener("blur",function(){document.getElementById("card-3d").classList.remove("flipped");});
updatePreview();

function showError(msg){
  document.getElementById("result").innerHTML='<div class="result-card result-error"><span style="color:#f87171;font-weight:600;">'+msg+'</span></div>';
}
function setLoading(on){
  var btn=document.getElementById("pay-btn");
  btn.disabled=on;
  document.getElementById("btn-spinner").style.display=on?"block":"none";
  document.getElementById("btn-text").textContent=on?"Processing…":"Pay Securely →";
}

// ── Confirmation modal ──
function showConfirm(){
  var rawAmt=document.getElementById("amount-display").value.replace(/,/g,"").trim();
  var amount=parseFloat(rawAmt);
  if(isNaN(amount)||amount<=0){showError("Please enter a valid amount (e.g. 500).");return;}
  if(!document.getElementById("first-name").value.trim()){showError("First name is required.");return;}
  if(!document.getElementById("last-name").value.trim()){showError("Last name is required.");return;}
  if(!document.getElementById("email").value.trim()){showError("Email is required.");return;}

  var fn=document.getElementById("first-name").value.trim();
  var ln=document.getElementById("last-name").value.trim();
  var email=document.getElementById("email").value.trim();
  var formatted="PHP "+amount.toLocaleString('en-PH',{minimumFractionDigits:2,maximumFractionDigits:2});

  var modal=document.createElement('div');
  modal.className='confirm-overlay';
  modal.id='confirm-modal';
  modal.innerHTML=
    '<div class="confirm-card" onclick="event.stopPropagation()">'+
      '<div class="confirm-icon">💳</div>'+
      '<div class="confirm-title">Confirm Payment</div>'+
      '<div class="confirm-sub">Please review your transaction details</div>'+
      '<div class="confirm-row"><span class="confirm-key">Name</span><span class="confirm-val">'+fn+' '+ln+'</span></div>'+
      '<div class="confirm-row"><span class="confirm-key">Email</span><span class="confirm-val">'+email+'</span></div>'+
      '<div class="confirm-row"><span class="confirm-key">Amount</span><span class="confirm-val confirm-amount">'+formatted+'</span></div>'+
      '<div class="confirm-actions">'+
        '<button class="btn-cancel" onclick="closeConfirm()">Cancel</button>'+
        '<button class="btn-confirm" onclick="proceedPayment()">Confirm →</button>'+
      '</div>'+
    '</div>';
  modal.onclick=function(e){if(e.target===modal)closeConfirm();};
  document.body.appendChild(modal);
}

function closeConfirm(){
  var m=document.getElementById('confirm-modal');
  if(m) m.remove();
}

function proceedPayment(){
  closeConfirm();
  var amount=parseFloat(document.getElementById("amount-display").value.replace(/,/g,"").trim());
  setLoading(true);
  if(window._simulate2d){
    document.getElementById("token-id").value="sim_tok_"+Date.now();
    document.getElementById("amount-hidden").value=amount;
    htmx.trigger(document.getElementById("checkout-form"),"submit");
    return;
  }
  var rawYear=document.getElementById("exp-year").value.trim();
  var expYear=rawYear.length<=2?"20"+rawYear.padStart(2,"0"):rawYear;
  var expMonth=document.getElementById("exp-month").value.trim().padStart(2,"0");
  Xendit.card.createToken({
    card_number:document.getElementById("card-number").value.replace(/\\s/g,""),
    card_exp_month:expMonth,card_exp_year:expYear,
    card_cvn:document.getElementById("cvn").value.trim(),
    card_holder_first_name:document.getElementById("first-name").value.trim(),
    card_holder_last_name:document.getElementById("last-name").value.trim(),
    card_holder_email:document.getElementById("email").value.trim(),
    amount:amount,is_multiple_use:false,should_authenticate:true,
  },function(err,token){
    if(err){showError(err.message);setLoading(false);return;}
    document.getElementById("token-id").value=token.id;
    document.getElementById("amount-hidden").value=amount;
    htmx.trigger(document.getElementById("checkout-form"),"submit");
  });
}

document.body.addEventListener("htmx:afterRequest",function(){
  setLoading(false);
  if(document.querySelector(".success-overlay")){
    launchConfetti();
    clearForm();
  }
});

function clearForm(){
  ["first-name","last-name","email","card-number","exp-month","exp-year","cvn","amount-display"].forEach(function(id){
    var el=document.getElementById(id);
    if(el) el.value="";
  });
  document.getElementById("token-id").value="";
  document.getElementById("amount-hidden").value="";
  updatePreview();
}

function closeSuccess(){
  var overlay=document.querySelector(".success-overlay");
  if(overlay) overlay.remove();
  document.getElementById("result").innerHTML="";
}

function launchConfetti(){
  var colors=['#00A896','#00BFA5','#4dd0c4','#b2dfdb','#ffffff','#80cbc4','#e0f2f1'];
  for(var i=0;i<90;i++){
    (function(i){
      setTimeout(function(){
        var el=document.createElement('div');
        var size=(Math.random()*9+4).toFixed(1);
        var isCircle=Math.random()>0.5;
        var duration=(Math.random()*1.8+1.8).toFixed(2);
        var left=(Math.random()*100).toFixed(1);
        var rotate=Math.floor(Math.random()*360);
        el.style.cssText='position:fixed;z-index:10001;pointer-events:none;top:-12px;left:'+left+'vw;width:'+size+'px;height:'+size+'px;background:'+colors[Math.floor(Math.random()*colors.length)]+';border-radius:'+(isCircle?'50%':'2px')+';transform:rotate('+rotate+'deg);transition:top '+duration+'s ease-in,opacity 0.4s ease '+(parseFloat(duration)-0.4).toFixed(2)+'s,transform '+duration+'s linear;';
        document.body.appendChild(el);
        requestAnimationFrame(function(){requestAnimationFrame(function(){
          el.style.top='108vh';el.style.opacity='0';el.style.transform='rotate('+(rotate+540)+'deg)';
        });});
        setTimeout(function(){el.remove();},(parseFloat(duration)+0.5)*1000);
      },i*18);
    })(i);
  }
}

if('serviceWorker'in navigator){
  window.addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});
}
"""


def checkout_page(public_key: str, simulate: bool = False) -> Html:
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1, viewport-fit=cover"),
            Title("Jade Gateway — Checkout"),
            Link(rel="manifest", href="/manifest.json"),
            Meta(name="theme-color", content="#00A896"),
            Meta(name="apple-mobile-web-app-capable", content="yes"),
            Meta(name="apple-mobile-web-app-status-bar-style", content="black-translucent"),
            Meta(name="apple-mobile-web-app-title", content="Jade Pay"),
            Link(rel="apple-touch-icon", href="/icon-maskable.svg"),
            Link(rel="icon", href="/icon.svg", type="image/svg+xml"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"),
            Script(src="https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js"),
            Script(src="https://js.xendit.co/v1/xendit.min.js"),
            Script(f"window._xenditPK='{public_key}';window._simulate2d={str(simulate).lower()};"),
            Style(STYLE),
        ),
        Body(
            Div(cls="orb orb-1"),
            Div(cls="orb orb-2"),
            Div(cls="orb orb-3"),
            Main(
                Div(
                    # Card preview
                    Div(
                        Div(
                            Div(
                                Div(
                                    Div(cls="card-chip"),
                                    Div(
                                        Span("))))", cls="card-contactless"),
                                        Span("JADE", cls="card-logo"),
                                        cls="card-logo-wrap",
                                    ),
                                    cls="card-top-row",
                                ),
                                Div("••••  ••••  ••••  ••••", id="preview-number", cls="card-number-preview"),
                                Div(
                                    Div(Div("Card Holder", cls="card-field-label"), Div("FULL NAME", id="preview-name", cls="card-field-value")),
                                    Div(Div("Expires", cls="card-field-label"), Div("MM/YY", id="preview-expiry", cls="card-field-value")),
                                    cls="card-bottom-row",
                                ),
                                cls="card-face card-front",
                            ),
                            Div(
                                Div(cls="card-stripe"),
                                Div(Span("•••", id="preview-cvv", cls="cvv-dots"), cls="cvv-strip"),
                                Div("JADE 2D Gateway", cls="card-back-footer"),
                                cls="card-face card-back",
                            ),
                            id="card-3d", cls="card-3d",
                        ),
                        cls="card-scene",
                    ),
                    # Form
                    Div(
                        Div(
                            Div(
                                Div(Span(cls="badge-dot"), "Secure Payment", cls="badge"),
                                H1("Checkout"),
                                P("2D · PCI-DSS 4.0.1 aligned", cls="subtitle"),
                                cls="header",
                            ),
                            Form(
                                Div("Cardholder", cls="section-label"),
                                Div(
                                    Div(Label("First Name"), Input(id="first-name", placeholder="Juan", autocomplete="cc-given-name"), cls="field"),
                                    Div(Label("Last Name"), Input(id="last-name", placeholder="dela Cruz", autocomplete="cc-family-name"), cls="field"),
                                    cls="row",
                                ),
                                Div(Label("Email"), Input(id="email", type="email", placeholder="juan@email.com", autocomplete="email", inputmode="email"), cls="field"),

                                Div("Card Details", cls="section-label"),
                                Div(Label("Card Number"), Input(id="card-number", placeholder="0000  0000  0000  0000", autocomplete="cc-number", inputmode="numeric"), cls="field"),
                                Div(
                                    Div(Label("Month"), Input(id="exp-month", placeholder="MM", autocomplete="cc-exp-month", inputmode="numeric"), cls="field"),
                                    Div(Label("Year"), Input(id="exp-year", placeholder="YY", autocomplete="cc-exp-year", inputmode="numeric"), cls="field"),
                                    Div(Label("CVV"), Input(id="cvn", type="password", placeholder="•••", autocomplete="cc-csc", inputmode="numeric"), cls="field"),
                                    cls="row",
                                ),

                                Div("Amount", cls="section-label"),
                                Div(Label("Amount (PHP)"), Input(id="amount-display", type="text", placeholder="e.g. 500", inputmode="decimal"), cls="field"),

                                Input(type="hidden", name="token_id", id="token-id"),
                                Input(type="hidden", name="amount", id="amount-hidden"),
                                Input(type="hidden", name="currency", value="PHP"),
                                Input(type="hidden", name="merchant_id", value="demo_merchant"),

                                Button(
                                    Div(Div(cls="spinner", id="btn-spinner"), Span("Pay Securely →", id="btn-text"), cls="btn-inner"),
                                    type="button", id="pay-btn", cls="jade-btn", onclick="showConfirm()",
                                ),
                                id="checkout-form",
                                hx_post="/api/v1/payments/charge",
                                hx_target="#result",
                                hx_swap="innerHTML",
                                novalidate=True,
                            ),
                            Div(id="result"),
                            Div(
                                Div(Span("🔒"), Span("256-bit SSL"), cls="security-item"),
                                Div(cls="security-dot"),
                                Div(Span("⚡"), Span("PCI-DSS 4.0.1"), cls="security-item"),
                                Div(cls="security-dot"),
                                Div(Span("🛡"), Span("Fraud Protected"), cls="security-item"),
                                cls="security-bar",
                            ),
                            cls="glass",
                        ),
                        cls="glass-wrap",
                    ),
                    cls="page-wrap",
                ),
            ),
            Script(SCRIPT),
        ),
    )
