// External Libraries
import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, ContactShadows, useProgress, Html } from '@react-three/drei';
import PropTypes from 'prop-types';

// Internal Modules
import GLBModel from "./GLB/GLB"
import OBJModel from "./OBJ/OBJ"

// Stylesheets
import "./Listing3D.scss"

const Loader = () => {
    const { progress } = useProgress();
    return <Html center>{ progress.toFixed(0) } % loaded</Html>;
};

const Listing3D = ({ modelPath }) => {
    return (
        <div className="listingShowcase">
            <Canvas camera={ { position: [0, 2, 5], fov: 45 } }>
                <Suspense fallback={ <Loader /> }>
                    { /* eslint-disable-next-line react/no-unknown-property */ }
                    <ambientLight intensity={ 0.5 } />
                    { /* eslint-disable-next-line react/no-unknown-property */ }
                    <directionalLight position={ [5, 5, 5] } intensity={ 1 } />

                    {modelPath.toLowerCase().endsWith(".glb") ? (
                        <GLBModel modelPath={ modelPath } />
                    ) : modelPath.toLowerCase().endsWith(".obj") ? (
                        <OBJModel modelPath={ modelPath } />
                    ) : (
                        <div>Unsupported model format: { modelPath }</div>
                    )}
                    <Environment preset="sunset" />
                    <ContactShadows position={ [0, -1.4, 0] } opacity={ 0.4 } scale={ 10 } blur={ 1.5 } far={ 4.5 } />
                    <OrbitControls enablePan enableZoom enableRotate />
                </Suspense>
            </Canvas>
        </div>
    );
};

Listing3D.propTypes = {
    modelPath: PropTypes.string.isRequired,
};

export default Listing3D;
