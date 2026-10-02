import type {ActionId,Context,HouseState,Placement} from './model';
import {applicableMemories} from './engine';
export type Pose='idle'|'left'|'right'|'reading'|'tea'|'welcome';
export type ResidentBeat={objectId:string;x:number;y:number;pose:Pose;label:string;reason:string};
export const roomVersions=[
 {id:'rain',name:'Rainy library',subtitle:'A quiet corner above the sleeping city.',image:'/house/room.webp',accent:'#bfd9ca'},
 {id:'glass',name:'Moonlit glasshouse',subtitle:'A room for green things and unhurried company.',image:'/house/glasshouse.webp',accent:'#bbdb9c'},
 {id:'amber',name:'Amber workshop',subtitle:'Unfinished ideas have somewhere to stay.',image:'/house/workshop.webp',accent:'#efbe83'}
] as const;
export type RoomVersion=typeof roomVersions[number]['id'];
function standingPoint(p:Placement){const offsets:Record<string,[number,number]>={'object-shelf':[1,17],'object-chair':[-8,7],'object-plant':[0,17],'object-memory':[-10,12]};const [dx,dy]=offsets[p.objectId]||[10,5];return {x:Math.max(24,Math.min(75,p.x+dx)),y:Math.max(61,Math.min(87,p.y+dy))}};
export function residentBeat(s:HouseState,c:Context,placements:Placement[],phase:number):ResidentBeat{
 const memories=applicableMemories(s,c),t=s.profile.traits;let objectId='object-desk',pose:Pose='reading',label='Returning to the open book',reason='This is a reading visit; the desk gives it a quiet centre.';
 if(memories.some(m=>m.effectId==='quiet-chair')&&phase%3===0){objectId='object-chair';pose='welcome';label='Leaving the quiet chair ready';reason='An approved memory applies to this kind of visit.'}
 else if(memories.some(m=>m.effectId==='add-plant')&&phase%3===1){objectId='object-plant';pose='idle';label='Checking the gift by the window';reason='The plant belongs here because its memory was approved.'}
 else if((memories.some(m=>m.effectId==='tea-for-two')||c.activity==='social'&&t.warmth>.65)&&phase%3===1){objectId='object-tea';pose='tea';label='Making room for a second cup';reason=memories.some(m=>m.effectId==='tea-for-two')?'A reviewed tea ritual is active.':'A hospitable personality gravitates toward the tea table.'}
 else if(c.activity==='social'&&t.sociability>.65&&phase%3!==2){objectId='object-chair';pose='welcome';label='Coming over to greet a visitor';reason='A sociable personality chooses the shared part of the room.'}
 else if(t.curiosity>.65&&phase%3===2){objectId='object-shelf';pose='reading';label='Following a half-remembered page';reason='Curiosity brings this resident back to the bookshelf.'}
 else if(t.order>.8){label='Putting one thought in order';reason='An orderly personality returns to a clear desk.'}
 const p=placements.find(p=>p.objectId===objectId&&p.visible)||placements.find(p=>p.objectId==='object-desk')!;
 return {objectId:p.objectId,...standingPoint(p),pose,label,reason};
}
export function encounterBeat(action:ActionId,stance:string,placements:Placement[]):ResidentBeat{
 const objects:Record<ActionId,string>={'sit-quietly':'object-chair','start-chat':'object-chair','share-tea':'object-tea','recommend-book':'object-shelf','offer-plant':'object-plant','interrupt-reading':'object-desk','leave-note':'object-desk'};
 const labels:Record<ActionId,string>={'sit-quietly':'A little room for quiet company','start-chat':'One small story, then','share-tea':'A cup on each side of the table','recommend-book':'Finding a place for the recommendation','offer-plant':'Considering the window corner','interrupt-reading':'Pausing at the edge of a reading hour','leave-note':'Reading the note, without learning it yet'};
 const p=placements.find(p=>p.objectId===objects[action])!;
 return {objectId:p.objectId,...standingPoint(p),pose:stance==='decline'?(action==='interrupt-reading'?'reading':'idle'):action==='share-tea'?'tea':action==='recommend-book'||action==='leave-note'?'reading':'welcome',label:stance==='decline'?'Leaving this invitation for another time':labels[action],reason:'Choreographed from the validated encounter. A response alone does not change lasting memory.'};
}
export function decorateRoom(placements:Placement[],version:RoomVersion):Placement[]{
 if(version==='rain')return placements;
 const offsets:Record<string,[number,number]>=version==='glass'?{'object-desk':[-5,1],'object-shelf':[5,1],'object-chair':[-1,4],'object-tea':[7,1],'object-memory':[-2,3]}:{'object-desk':[5,1],'object-shelf':[7,2],'object-chair':[5,3],'object-tea':[-4,1],'object-memory':[-3,0]};
 return placements.map(p=>{const d=offsets[p.objectId]||[0,0];return {...p,x:p.x+d[0],y:p.y+d[1]}});
}
