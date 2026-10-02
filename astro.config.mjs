import {defineConfig} from 'astro/config';import react from '@astrojs/react';import sanity from '@sanity/astro';
export default defineConfig({integrations:[sanity({projectId:'1jby3mjo',dataset:'production',apiVersion:'2026-10-01',useCdn:false,studioBasePath:'/desk',studioRouterHistory:'hash'}),react()],output:'static'});
