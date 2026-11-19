// Användning: node tools/html_to_pdf.js <utfil.pdf> "<sidfotstext>"
const {chromium}=require('playwright'); const path=require('path'); const R=path.resolve(__dirname,'..');
const out=process.argv[2]||'RL6000_MkII_forstudie_revA.pdf', foot=process.argv[3]||'RL6000 MkII – förstudie rev A';
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+R+'/_report.html');
await p.pdf({path:path.join(R,out),format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:7pt;width:100%;text-align:center;color:#888">'+foot+' · sida <span class="pageNumber"></span>/<span class="totalPages"></span></div>',margin:{top:'16mm',bottom:'16mm',left:'15mm',right:'15mm'}});
await b.close();})();
