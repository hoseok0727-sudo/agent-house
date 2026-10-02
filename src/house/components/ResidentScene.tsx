import {useEffect,useMemo,useState} from 'react';
import type {ActionId,Context,HouseState,Placement} from '../lib/model';
import {residentBeat,encounterBeat,type Pose} from '../lib/resident';
export type SceneEncounter={id:string;action:ActionId;stance:string;authoredStory?:boolean};
export default function ResidentScene({state,context,placements,encounter,busy,paused,onInspect}:{state:HouseState;context:Context;placements:Placement[];encounter:SceneEncounter|null;busy:boolean;paused:boolean;onInspect:(id:string)=>void}){
 const [phase,setPhase]=useState(0),[scene,setScene]=useState<SceneEncounter|null>(null),[moving,setMoving]=useState(false),[reduced,setReduced]=useState(false);
 useEffect(()=>{if(!window.matchMedia)return;const q=window.matchMedia('(prefers-reduced-motion: reduce)');setReduced(q.matches);const change=()=>setReduced(q.matches);q.addEventListener('change',change);return()=>q.removeEventListener('change',change)},[]);
 useEffect(()=>{setPhase(0);setScene(null)},[context.time,context.activity,state.profile.name,state.snapshot.edition]);
 useEffect(()=>{if(paused||reduced||busy||scene)return;const timer=setInterval(()=>setPhase(p=>p+1),8500);return()=>clearInterval(timer)},[paused,reduced,busy,scene]);
 useEffect(()=>{setScene(encounter);if(!encounter)return;const timer=setTimeout(()=>setScene(null),9000);return()=>clearTimeout(timer)},[encounter]);
 const beat=useMemo(()=>{if(scene){const b=encounterBeat(scene.action,scene.stance,placements);return scene.authoredStory?{...b,label:'Looking for the next story clue',reason:'An authored mini-story. Inspecting a clue creates no encounter or learned memory.'}:b}return residentBeat(state,context,placements,phase)},[scene,state,context,placements,phase]);
 useEffect(()=>{if(reduced){setMoving(false);return}setMoving(true);const timer=setTimeout(()=>setMoving(false),1400);return()=>clearTimeout(timer)},[beat.x,beat.y,reduced]);
 const poses:Record<Pose,number>={idle:0,left:1,right:2,reading:3,tea:4,welcome:5};const index=!reduced&&moving?(beat.x<50?1:2):poses[beat.pose];
 return <><button className={'ah-resident-character '+(!reduced&&moving?'walking':'resting')} style={{left:beat.x+'%',top:beat.y+'%',zIndex:Math.round(beat.y)+2,backgroundPosition:`${index%3*50}% ${Math.floor(index/3)*100}%`}} aria-label={`${state.profile.name}: ${busy?'Considering the encounter':beat.label}. Inspect this activity.`} onClick={()=>onInspect(beat.objectId)}><span className="ah-resident-name">{state.profile.name}</span></button><div className="ah-activity"><span className="ah-activity-kicker">{busy?'CONSIDERING THE ENCOUNTER':scene?.authoredStory?'A STORY IN THE ROOM':scene?'A MOMENT TOGETHER':'LIFE IN THE ROOM'}</span><strong>{busy?'A little time to consider…':beat.label}</strong><details><summary>Why this activity?</summary><p>{beat.reason}</p><small>Personality-driven choreography. {paused||reduced?'Automatic routine paused.':'No background AI requests.'}</small></details></div></>;
}
