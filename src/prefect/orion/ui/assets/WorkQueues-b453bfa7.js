import{d as i,$ as f,a0 as _,c as a,a as u,w as n,a2 as b,o,b as v,u as e,b0 as w,h as y,b1 as Q,b2 as x,a6 as g,e as h}from"./index-3e9b5a4f-22e45b7a.js";import{u as C}from"./usePageTitle-9cf51495.js";const N=i({__name:"WorkQueues",setup(q){const l=f(),p={interval:3e4},s=_(l.workQueues.getWorkQueues,[{}],p),r=a(()=>s.response??[]),c=a(()=>s.executed&&r.value.length==0),d=a(()=>s.executed);return C("Work Queues"),(B,t)=>{const m=b("p-layout-default");return o(),u(m,{class:"queues"},{header:n(()=>[v(e(w))]),default:n(()=>[e(d)?(o(),y(g,{key:0},[e(c)?(o(),u(e(Q),{key:0})):(o(),u(e(x),{key:1,"work-queues":e(r),onUpdate:t[0]||(t[0]=k=>e(s).refresh()),onDelete:t[1]||(t[1]=k=>e(s).refresh())},null,8,["work-queues"]))],64)):h("",!0)]),_:1})}}});export{N as default};
