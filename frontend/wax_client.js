import {api} from './base.js';
const base='/api/wax-batches';
export const batches=()=>api(base);
export const data=(key,part)=>api(`${base}/${key}/${part}`);
export const save=(key,part,body)=>api(`${base}/${key}/${part}`,part==='readings'?'PUT':'POST',body);
