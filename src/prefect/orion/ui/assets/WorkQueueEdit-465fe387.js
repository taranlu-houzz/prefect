import{d as m,$ as _,al as w,f,a as Q,w as l,a2 as y,o as b,b as p,u,ba as h,bb as q,K as i}from"./index-3e9b5a4f-22e45b7a.js";import{u as C}from"./usePageTitle-9cf51495.js";import{r as g}from"./index-8ec704cb.js";import"./routes-f61735ce.js";import"./meta-26546594.js";const I=m({__name:"WorkQueueEdit",async setup(x){let e,r;const a=_(),t=w("workQueueId"),o=([e,r]=f(()=>a.workQueues.getWorkQueue(t.value)),e=await e,r(),e),s=()=>{g.back()},d=async n=>{try{await a.workQueues.updateWorkQueue(t.value,n),i(`${o.name} updated`,"success"),s()}catch(c){i("Error occurred while updating your queue","error"),console.error(c)}};return C(`Edit Work Queue: ${o.name}`),(n,c)=>{const k=y("p-layout-default");return b(),Q(k,null,{header:l(()=>[p(u(h),{"work-queue":u(o)},null,8,["work-queue"])]),default:l(()=>[p(u(q),{"work-queue":u(o),onSubmit:d,onCancel:s},null,8,["work-queue"])]),_:1})}}});export{I as default};
