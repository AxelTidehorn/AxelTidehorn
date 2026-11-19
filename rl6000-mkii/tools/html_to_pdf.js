const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file:///home/user/AxelTidehorn/rl6000-mkii/_report.html');
await p.pdf({path:'/home/user/AxelTidehorn/rl6000-mkii/RL6000_MkII_forstudie_revA.pdf',format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:7pt;width:100%;text-align:center;color:#888">RL6000 MkII – förstudie rev A · sida <span class="pageNumber"></span>/<span class="totalPages"></span></div>',margin:{top:'16mm',bottom:'16mm',left:'15mm',right:'15mm'}});
await b.close();})();
