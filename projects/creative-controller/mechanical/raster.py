"""Tiny numpy z-buffer rasterizer: smooth-shaded, SSAA, perspective. No GPU/OpenGL needed."""
import numpy as np, trimesh
from PIL import Image
def look_at(eye, target, up=(0,0,1)):
    f = np.array(target,float)-eye; f/=np.linalg.norm(f); r=np.cross(f,up); r/=np.linalg.norm(r); u=np.cross(r,f)
    return np.array([r,u,-f]), np.array(eye,float)
def render(items, fname, eye, target=(0,0,10), W=1400, H=1050, ss=2, fov=28, bg=(246,246,248)):
    w,h = W*ss, H*ss
    zb = np.full((h,w), np.inf); img = np.zeros((h,w,3)); img[:] = np.array(bg)/255
    R,E = look_at(np.array(eye,float), target); f = 0.5*h/np.tan(np.radians(fov/2))
    L1 = np.array([-0.4,-0.6,0.9]); L1/=np.linalg.norm(L1); L2=np.array([0.7,0.3,0.4]); L2/=np.linalg.norm(L2)
    for mesh, color, spec in items:
        m = mesh.smooth_shaded if len(mesh.faces) < 200000 else mesh
        V = m.vertices; N = m.vertex_normals; F = m.faces
        cam = (V-E)@R.T; z = -cam[:,2]
        sx = w/2 + f*cam[:,0]/z; sy = h/2 - f*cam[:,1]/z
        col = np.array(color,float)
        vd = E - V; vd /= np.linalg.norm(vd,axis=1)[:,None]
        d = np.clip(N@L1,0,1)*0.75 + np.clip(N@L2,0,1)*0.25
        hv = (L1[None]+vd); hv/=np.linalg.norm(hv,axis=1)[:,None]
        sp = np.clip((N*hv).sum(1),0,1)**40*spec
        rim = (1-np.clip((N*vd).sum(1),0,1))**3*0.15
        shade = np.clip(col[None]*(0.32+0.75*d[:,None]) + sp[:,None] + rim[:,None],0,1)
        for t in F:
            x = sx[t]; y = sy[t]; zz = z[t]
            x0,x1 = int(max(np.floor(x.min()),0)), int(min(np.ceil(x.max()),w-1)); y0,y1 = int(max(np.floor(y.min()),0)), int(min(np.ceil(y.max()),h-1))
            if x0>x1 or y0>y1 or zz.min()<=0: continue
            den = (y[1]-y[2])*(x[0]-x[2])+(x[2]-x[1])*(y[0]-y[2])
            if abs(den) < 1e-9: continue
            X,Y = np.meshgrid(np.arange(x0,x1+1)+0.5, np.arange(y0,y1+1)+0.5)
            a = ((y[1]-y[2])*(X-x[2])+(x[2]-x[1])*(Y-y[2]))/den; b = ((y[2]-y[0])*(X-x[2])+(x[0]-x[2])*(Y-y[2]))/den; c = 1-a-b
            msk = (a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)
            if not msk.any(): continue
            iz = a/zz[0]+b/zz[1]+c/zz[2]; depth = 1/iz
            sub = zb[y0:y1+1, x0:x1+1]; upd = msk & (depth < sub)
            if not upd.any(): continue
            sub[upd] = depth[upd]
            s = shade[t]; px = (a[...,None]*s[0]+b[...,None]*s[1]+c[...,None]*s[2])
            img[y0:y1+1, x0:x1+1][upd] = px[upd]
    # soft ground shadow-ish vignette skipped; downsample
    out = (img.reshape(H,ss,W,ss,3).mean((1,3))*255).astype(np.uint8)
    Image.fromarray(out).save(fname)
