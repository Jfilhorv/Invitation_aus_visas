(()=>{
  "use strict";
  const rows=(window.CONVITES_DATA||[]).filter(row=>String(row.validado)==="true");
  const nodes=window.ANZSCO_HIERARCHY?.nodes||{};
  const scopes=["FEDERAL","WA","ACT"];
  const metrics={FEDERAL:"pontos_minimos",WA:"ultimo_eoi_pontos",ACT:"matrix_score"};
  const metricLabels={pontos_minimos:"Minimum points",ultimo_eoi_pontos:"Last invited EOI points",matrix_score:"Canberra Matrix score"};
  const levelLabels={FEDERAL:"Occupation",WA:"Occupation",ACT:"Unit group"};
  let scope="ALL";
  const $=id=>document.getElementById(id);
  const extra=value=>Object.fromEntries(String(value||"").split(";").map(part=>part.split("=",2).map(item=>item.trim())).filter(pair=>pair.length===2));
  const validDate=value=>/^\d{4}-\d{2}(?:-\d{2})?$/.test(String(value||""));
  const num=value=>{const result=Number(String(value).replaceAll(",",""));return Number.isFinite(result)?result:null};
  const median=values=>{const sorted=values.filter(Number.isFinite).sort((a,b)=>a-b);return sorted.length?sorted[Math.floor((sorted.length-1)/2)]:null};
  const esc=value=>String(value??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
  const fmt=value=>value==null?"—":new Intl.NumberFormat("en-AU",{maximumFractionDigits:1}).format(value);
  const dateLabel=value=>{
    if(/^\d{4}-\d{2}-\d{2}$/.test(value||""))return new Intl.DateTimeFormat("en-AU",{day:"numeric",month:"short",year:"numeric",timeZone:"UTC"}).format(new Date(`${value}T00:00:00Z`));
    if(/^\d{4}-\d{2}$/.test(value||""))return new Intl.DateTimeFormat("en-AU",{month:"short",year:"numeric",timeZone:"UTC"}).format(new Date(`${value}-01T00:00:00Z`));
    return value||"Not available";
  };
  const resultRows=rows.filter(row=>{
    const value=num(row.valor);
    return scopes.includes(row.jurisdicao)&&row.metrica===metrics[row.jurisdicao]&&row.ocupacao!=="agregado"&&value>0&&value<=200&&validDate(row.data_round);
  });
  const selectedScopes=()=>scope==="ALL"?scopes:[scope];
  const scopedResults=()=>resultRows.filter(row=>selectedScopes().includes(row.jurisdicao));
  const identity=row=>row.ocupacao==="Painting Trades Worker"&&!row.anzsco
    ?"ANZSCO-2022:332211"
    :row.identidade_ocupacional||`${row.jurisdicao}:${row.anzsco||row.ocupacao}`;
  function roundContext(row){
    const fields=extra(row.unidade_extra);
    const parts=[row.jurisdicao||"",row.visto||"",row.metrica||"",row.nivel_ocupacional||""];
    if(row.jurisdicao==="FEDERAL")parts.push(String(fields.location||fields.applicant_location||"").toLowerCase());
    if(row.jurisdicao==="WA")parts.push(fields.stream||"",fields.residence||"",fields.priority||"");
    if(row.jurisdicao==="ACT")parts.push(fields.residence||fields.applicant||fields.applicant_location||"");
    return parts.join("|");
  }
  const compareKey=row=>`${identity(row)}|${roundContext(row)}`;

  function overviewCard(jurisdiction){
    const source=resultRows.filter(row=>row.jurisdicao===jurisdiction);
    const dates=[...new Set(source.map(row=>row.data_round))].sort();
    const latest=dates.at(-1)||"";
    const latestRows=source.filter(row=>row.data_round===latest);
    const evidence=latestRows[0]?.fonte_url||"";
    return `<article class="card overview-card">
      <div class="scope-kicker">${jurisdiction==="FEDERAL"?"FED":jurisdiction}<span>${levelLabels[jurisdiction]}</span></div>
      <strong class="latest">${esc(dateLabel(latest))}</strong><small>latest official score result</small>
      <div class="meta-list">
        <div class="meta-row"><span>Coverage</span><b>${fmt(new Set(source.map(identity)).size)} identities · ${fmt(new Set(source.map(row=>row.data_round)).size)} rounds</b></div>
        <div class="meta-row"><span>Metric</span><b>${metricLabels[metrics[jurisdiction]]}</b></div>
        <div class="meta-row"><span>Latest result rows</span><b>${fmt(latestRows.length)}</b></div>
        <div class="meta-row"><span>Evidence</span><b>${evidence?`<a class="source-link" href="${esc(evidence)}" target="_blank" rel="noopener">Official source ↗</a>`:"Not available"}</b></div>
      </div></article>`;
  }
  function renderOverview(){
    $("overviewGrid").innerHTML=selectedScopes().map(overviewCard).join("");
    $("scopeNote").textContent=scope==="ALL"
      ?"ALL is a coverage panorama across FED, WA and ACT. Score trends remain separated by jurisdiction."
      :`${scope==="FEDERAL"?"FED":scope} uses ${metricLabels[metrics[scope]].toLowerCase()} at ${levelLabels[scope].toLowerCase()} level.`;
  }

  function previousComparable(jurisdiction){
    const source=resultRows.filter(row=>row.jurisdicao===jurisdiction);
    const dates=[...new Set(source.map(row=>row.data_round))].sort();
    const latest=dates.at(-1)||"";
    const current=source.filter(row=>row.data_round===latest);
    const currentByKey=new Map(current.map(row=>[compareKey(row),row]));
    for(const date of dates.slice(0,-1).reverse()){
      const previousByKey=new Map(source.filter(row=>row.data_round===date).map(row=>[compareKey(row),row]));
      const deltas=[...currentByKey].flatMap(([key,row])=>previousByKey.has(key)?[num(row.valor)-num(previousByKey.get(key).valor)]:[]);
      if(deltas.length)return {
        latest,current,date,matched:deltas.length,delta:median(deltas),
        lower:deltas.filter(value=>value<0).length,
        unchanged:deltas.filter(value=>value===0).length,
        higher:deltas.filter(value=>value>0).length
      };
    }
    return {latest,current,date:"",matched:0,delta:null,lower:0,unchanged:0,higher:0};
  }
  function yoyComparable(jurisdiction,latest,current){
    const match=String(latest||"").match(/^(\d{4})-(\d{2})/);
    if(!match)return null;
    const prefix=`${Number(match[1])-1}-${match[2]}`;
    const pastByKey=new Map(resultRows.filter(row=>row.jurisdicao===jurisdiction&&String(row.data_round).startsWith(prefix)).map(row=>[compareKey(row),row]));
    const deltas=current.flatMap(row=>pastByKey.has(compareKey(row))?[num(row.valor)-num(pastByKey.get(compareKey(row)).valor)]:[]);
    return deltas.length?{matched:deltas.length,delta:median(deltas)}:null;
  }
  function monthlyChange(jurisdiction){
    const monthly=rows.filter(row=>row.jurisdicao===jurisdiction&&/^\d{4}-\d{2}$/.test(row.data_round||"")&&String(row.ocupacao).toLowerCase()==="agregado"&&["convites_emitidos","eois_convidados"].includes(row.metrica)&&num(row.valor)!=null);
    const totals=new Map();
    monthly.forEach(row=>totals.set(row.data_round,(totals.get(row.data_round)||0)+num(row.valor)));
    const dates=[...totals.keys()].sort();
    if(dates.length<2)return null;
    const [previousDate,date]=dates.slice(-2);
    const [ay,am]=previousDate.split("-").map(Number),[by,bm]=date.split("-").map(Number);
    if((by-ay)*12+bm-am!==1)return null;
    return {date,previousDate,delta:totals.get(date)-totals.get(previousDate)};
  }
  function trendCard(jurisdiction){
    const comparison=previousComparable(jurisdiction);
    const currentMedian=median(comparison.current.map(row=>num(row.valor)));
    const yoy=yoyComparable(jurisdiction,comparison.latest,comparison.current);
    const monthly=monthlyChange(jurisdiction);
    const movement=comparison.delta===0
      ?"<b>Median unchanged (0 points)</b>. Some matched contexts may still have moved."
      :`Median change: <b>${comparison.delta>0?"+":""}${fmt(comparison.delta)} points</b>.`;
    return `<article class="card trend-card"><div class="scope-kicker">${jurisdiction==="FEDERAL"?"FED":jurisdiction}<span>${metricLabels[metrics[jurisdiction]]}</span></div>
      <div class="trend-value"><strong>${fmt(currentMedian)}</strong><span>median published score<br>${esc(dateLabel(comparison.latest))}</span></div>
      <div class="comparison">${comparison.matched
        ?`${movement}<br>${fmt(comparison.matched)} matched ${comparison.matched===1?"context":"contexts"}: latest ${esc(dateLabel(comparison.latest))} vs previous ${esc(dateLabel(comparison.date))}.<div class="distribution" aria-label="Matched context distribution"><span class="lower">↓ ${comparison.lower} lower</span><span>→ ${comparison.unchanged} unchanged</span><span class="higher">↑ ${comparison.higher} higher</span></div>`
        :`Previous comparable round: <b>No matching context</b> for ${esc(dateLabel(comparison.latest))}.`}</div>
      <div class="availability"><div><span>Year on year</span><b>${yoy?`${yoy.delta>0?"+":""}${fmt(yoy.delta)} points · ${yoy.matched} matched`:"No matching context one year earlier"}</b></div>
      <div><span>Official monthly total</span><b>${monthly?`${monthly.delta>0?"+":""}${fmt(monthly.delta)} · ${esc(dateLabel(monthly.date))} vs ${esc(dateLabel(monthly.previousDate))}`:"No consecutive official monthly totals"}</b></div></div>
    </article>`;
  }
  function renderTrends(){$("trendGrid").innerHTML=selectedScopes().map(trendCard).join("")}

  const pretty=value=>({"189":"189","491-family":"491 family","n/a":"Visa not separated",onshore:"Onshore",offshore:"Offshore",WASMOL1:"WASMOL Schedule 1",WASMOL2:"WASMOL Schedule 2",graduate_he:"Graduate · Higher Ed",graduate_vet:"Graduate · VET",WA:"WA resident",Overseas:"Overseas","Another Australian State or Territory":"Interstate",canberra_resident:"Canberra resident",overseas:"Overseas"})[value]||String(value||"Not stated").replaceAll("_"," ");
  function storyItems(jurisdiction){
    const counts=new Map();
    const add=label=>counts.set(label,(counts.get(label)||0)+1);
    resultRows.filter(row=>row.jurisdicao===jurisdiction).forEach(row=>{
      const fields=extra(row.unidade_extra);
      if(jurisdiction==="FEDERAL"){add(pretty(row.visto));if(fields.location)add(pretty(fields.location.toLowerCase()))}
      else if(jurisdiction==="WA"){if(fields.stream)add(pretty(fields.stream));if(fields.residence)add(pretty(fields.residence))}
      else{const applicant=fields.applicant||fields.applicant_location||fields.residence;if(applicant)add(pretty(applicant.toLowerCase()))}
    });
    return [...counts].sort((a,b)=>b[1]-a[1]);
  }
  function barsMarkup(items,percent=false){
    const max=Math.max(1,...items.map(item=>item[1])),total=items.reduce((sum,item)=>sum+item[1],0);
    return items.length?`<div class="bars">${items.map(([label,value])=>`<div class="bar-row" title="${esc(label)}: ${fmt(value)}"><span class="bar-label">${esc(label)}</span><span class="track"><span class="fill" style="width:${100*value/max}%"></span></span><span class="bar-value">${percent?`${Math.round(100*value/Math.max(total,1))}%`:fmt(value)}</span></div>`).join("")}</div>`:'<div class="empty">No published rows are available for this scope.</div>';
  }
  function renderStories(){
    $("storyGrid").innerHTML=selectedScopes().map(jurisdiction=>`<article class="card story-card"><div class="scope-kicker">${jurisdiction==="FEDERAL"?"FED":jurisdiction}<span>result rows</span></div><h3>${jurisdiction==="FEDERAL"?"Visa and applicant location":jurisdiction==="WA"?"Stream and residence":"Applicant location"}</h3>${barsMarkup(storyItems(jurisdiction))}</article>`).join("");
  }

  function rowCode(row){return row.ocupacao==="Painting Trades Worker"&&!row.anzsco?"332211":String(row.anzsco||"").replace(/\D/g,"")}
  function coverageCount(prefix){
    return new Set(scopedResults().filter(row=>rowCode(row).startsWith(prefix)).map(row=>`${row.jurisdicao}|${row.data_round}|${identity(row)}|${roundContext(row)}`)).size;
  }
  function renderTree(){
    const majors=Object.entries(nodes).filter(([code,node])=>code.length===1&&node.level==="major").sort(([a],[b])=>a.localeCompare(b));
    const majorCounts=majors.map(([code])=>coverageCount(code));
    const maxMajor=Math.max(1,...majorCounts);
    $("treeNote").textContent=`${scope==="ALL"?"ALL keeps FED, WA and ACT semantically separate. ":""}Counts show publication-row coverage, not invitation volumes.`;
    $("drillTree").innerHTML=majors.map(([code,node],index)=>{
      const subMajors=Object.entries(nodes).filter(([subCode,subNode])=>subCode.length===2&&subNode.level==="sub_major"&&subCode.startsWith(code)).sort(([a],[b])=>a.localeCompare(b));
      const subCounts=subMajors.map(([subCode])=>coverageCount(subCode));
      const maxSub=Math.max(1,...subCounts);
      return `<details class="major-branch" open><summary class="major-summary"><span class="tree-code">${code}</span><span class="tree-name">${esc(node.name)}</span><span class="tree-track"><span class="tree-fill" style="width:${100*majorCounts[index]/maxMajor}%"></span></span><span class="tree-count">${fmt(majorCounts[index])} rows</span></summary><div class="sub-tree">${subMajors.map(([subCode,subNode],subIndex)=>`<div class="sub-row${subCounts[subIndex]?"":" zero"}"><span class="tree-code">${subCode}</span><span class="tree-name">${esc(subNode.name)}</span><span class="tree-track"><span class="tree-fill" style="width:${100*subCounts[subIndex]/maxSub}%"></span></span><span class="tree-count">${fmt(subCounts[subIndex])} rows</span></div>`).join("")}</div></details>`;
    }).join("");
  }

  function renderLegacy(){
    const isResult=row=>["pontos_minimos","matrix_score","ultimo_eoi_pontos"].includes(row.metrica);
    $("kRows").textContent=fmt(rows.length);
    $("kOcc").textContent=fmt(new Set(resultRows.map(identity)).size);
    $("kDates").textContent=fmt(new Set(rows.filter(isResult).map(row=>row.data_round).filter(Boolean)).size);
    $("kSources").textContent=fmt(new Set(rows.map(row=>row.fonte_url).filter(Boolean)).size);
    $("topMeta").textContent=`${new Set(resultRows.map(identity)).size} occupations · ${resultRows.length} official score rows`;
    const coverage={FEDERAL:["live","Occupation scores + invitation totals"],ACT:["live","Matrix cut-offs by ANZSCO group"],WA:["live","Last invited EOI + aggregate totals"],SA:["live","Invitation counts by ANZSCO group"],NSW:["context","Skills lists + allocations"],VIC:["context","Priorities + allocations"],QLD:["context","Occupation lists + allocations"],TAS:["context","ROI and allocation totals"],NT:["context","Program context; no results table"]};
    $("coverageGrid").innerHTML=Object.entries(coverage).map(([key,value])=>`<div class="state ${value[0]}"><div class="state-code">${key}<span class="dot"></span></div><p>${value[1]}</p><b>${value[0]==="live"?"Analytical data":"Context only"}</b></div>`).join("");
    const aggregate=rows.filter(row=>["convites_emitidos","eois_convidados"].includes(row.metrica)&&String(row.ocupacao).toLowerCase()==="agregado"&&num(row.valor)!=null);
    const sumBy=(source,key)=>Object.entries(source.reduce((output,row)=>(output[key(row)]=(output[key(row)]||0)+num(row.valor),output),{})).sort((a,b)=>b[1]-a[1]);
    $("volumeState").innerHTML=barsMarkup(sumBy(aggregate,row=>row.jurisdicao));
    $("volumeVisa").innerHTML=barsMarkup(sumBy(aggregate,row=>row.visto));
    const groupNames={13:"Specialist Managers",14:"Hospitality & Service Managers",22:"Business & Marketing Professionals",23:"Engineering & Science Professionals",24:"Education Professionals",25:"Health Professionals",26:"ICT Professionals",27:"Legal & Welfare Professionals",31:"Engineering & Science Technicians",32:"Automotive & Engineering Trades",33:"Construction Trades",34:"Electrotechnology Trades",35:"Food Trades",41:"Health & Welfare Support"};
    const distinct={};
    rows.filter(isResult).filter(row=>/^\d{2,6}$/.test(row.anzsco||"")).forEach(row=>{const group=row.anzsco.slice(0,2);distinct[`${group}|${identity(row)}`]=group});
    const grouped=Object.values(distinct).reduce((output,group)=>(output[group]=(output[group]||0)+1,output),{});
    $("groups").innerHTML=barsMarkup(Object.entries(grouped).sort((a,b)=>b[1]-a[1]).slice(0,12).map(([group,count])=>[`${group} · ${nodes[group]?.name||groupNames[group]||"Other ANZSCO group"}`,count]),true);
    const wa=rows.filter(row=>row.jurisdicao==="WA"&&row.metrica==="ultimo_eoi_pontos"&&num(row.valor)!=null);
    const countExtra=key=>Object.entries(wa.reduce((output,row)=>{const value=extra(row.unidade_extra)[key]||"Not stated";output[value]=(output[value]||0)+1;return output},{})).sort((a,b)=>b[1]-a[1]);
    $("waResidence").innerHTML=barsMarkup(countExtra("residence"),true);
    $("waStream").innerHTML=barsMarkup(countExtra("stream"),true);
    const bands={"65–69":0,"70–79":0,"80–89":0,"90+":0};
    wa.forEach(row=>{const value=num(row.valor);bands[value>=90?"90+":value>=80?"80–89":value>=70?"70–79":"65–69"]++});
    $("waScore").innerHTML=barsMarkup(Object.entries(bands),true);
    const ages=wa.map(row=>{const submitted=extra(row.unidade_extra).eoi_submission_date;if(!submitted||!row.data_round)return null;const round=new Date(row.data_round.length===7?`${row.data_round}-28`:row.data_round);const days=(round-new Date(submitted))/86400000;return days>=0?days:null}).filter(Number.isFinite).sort((a,b)=>a-b);
    const ageMedian=ages.length?ages[Math.floor(ages.length/2)]:null;
    $("waAge").innerHTML=`<b>EOI queue age:</b> the median published last-invited EOI was approximately <b>${ageMedian==null?"not available":`${fmt(ageMedian)} days old`}</b> at the represented WA round. Month-only round dates make this an estimate, not an exact waiting time.`;
  }

  function render(){renderOverview();renderTrends();renderStories();renderTree()}
  function setScope(next){
    scope=scopes.includes(next)?next:"ALL";
    document.querySelectorAll("[data-scope]").forEach(button=>button.setAttribute("aria-pressed",String(button.dataset.scope===scope)));
    render();
  }
  document.querySelectorAll("[data-scope]").forEach(button=>button.addEventListener("click",()=>setScope(button.dataset.scope)));
  $("scopeSegment").addEventListener("keydown",event=>{
    if(!["ArrowLeft","ArrowRight","Home","End"].includes(event.key))return;
    const buttons=[...document.querySelectorAll("[data-scope]")],current=buttons.indexOf(document.activeElement);
    if(current<0)return;
    event.preventDefault();
    const index=event.key==="Home"?0:event.key==="End"?buttons.length-1:(current+(event.key==="ArrowRight"?1:-1)+buttons.length)%buttons.length;
    buttons[index].focus();buttons[index].click();
  });
  function applyTheme(theme){
    const next=theme==="dark"?"dark":"light";
    document.documentElement.dataset.theme=next;
    try{localStorage.setItem("convites-theme",next)}catch(_){}
    $("themeLight").classList.toggle("on",next==="light");$("themeDark").classList.toggle("on",next==="dark");
  }
  $("themeLight").addEventListener("click",()=>applyTheme("light"));
  $("themeDark").addEventListener("click",()=>applyTheme("dark"));
  let saved="light";try{saved=localStorage.getItem("convites-theme")||localStorage.getItem("invitation-theme")||"light"}catch(_){}
  applyTheme(saved);
  renderLegacy();
  render();

  const reduced=window.matchMedia("(prefers-reduced-motion: reduce)");
  if(!reduced.matches&&window.matchMedia("(hover:hover) and (pointer:fine)").matches){
    document.querySelectorAll(".kpi").forEach(card=>{
      card.addEventListener("pointermove",event=>{const box=card.getBoundingClientRect(),x=(event.clientX-box.left)/box.width-.5,y=(event.clientY-box.top)/box.height-.5;card.style.setProperty("--kpi-ry",`${(x*12).toFixed(2)}deg`);card.style.setProperty("--kpi-rx",`${(-y*10).toFixed(2)}deg`)});
      card.addEventListener("pointerleave",()=>{card.style.setProperty("--kpi-rx","0deg");card.style.setProperty("--kpi-ry","0deg")});
    });
    document.querySelectorAll(".brand-mark,.brand-copy").forEach(item=>{
      item.addEventListener("pointermove",event=>{const box=item.getBoundingClientRect(),x=(event.clientX-box.left)/box.width-.5,y=(event.clientY-box.top)/box.height-.5;item.style.setProperty("--brand-ry",`${(x*7).toFixed(2)}deg`);item.style.setProperty("--brand-rx",`${(-y*6).toFixed(2)}deg`)});
      item.addEventListener("pointerleave",()=>{item.style.setProperty("--brand-rx","0deg");item.style.setProperty("--brand-ry","0deg")});
    });
    document.querySelectorAll(".ias-explainer").forEach(card=>{
      card.addEventListener("pointermove",event=>{const box=card.getBoundingClientRect(),x=(event.clientX-box.left)/box.width-.5,y=(event.clientY-box.top)/box.height-.5;card.style.setProperty("--ias-card-ry",`${(x*5).toFixed(2)}deg`);card.style.setProperty("--ias-card-rx",`${(-y*4).toFixed(2)}deg`)});
      card.addEventListener("pointerleave",()=>{card.style.setProperty("--ias-card-rx","0deg");card.style.setProperty("--ias-card-ry","0deg")});
    });
  }
})();
