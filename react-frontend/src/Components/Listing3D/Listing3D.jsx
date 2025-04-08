// External Libraries
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment, ContactShadows, useGLTF, useProgress, Html } from '@react-three/drei';
import { Suspense } from 'react';
import PropTypes from 'prop-types';

// Stylesheets
import "./Listing3D.scss"

const Model = ({ url }) => {
    const { scene } = useGLTF(url);
    // eslint-disable-next-line react/no-unknown-property
    return <primitive object={scene} />;
};

const Loader = () => {
    const { progress } = useProgress();
    return <Html center>{progress.toFixed(0)} % loaded</Html>;
};

const Listing3D = ({ modelPath }) => {
    return (
        <div className="listingShowcase">
            <Canvas camera={{ position: [0, 2, 5], fov: 45 }}>
                <Suspense fallback={<Loader />}>
                    {/* eslint-disable-next-line react/no-unknown-property */}
                    <ambientLight intensity={0.5} />
                    {/* eslint-disable-next-line react/no-unknown-property */}
                    <directionalLight position={[5, 5, 5]} intensity={1} />
                    <Model url={modelPath} />
                    <Environment preset="sunset" />
                    <ContactShadows position={[0, -1.4, 0]} opacity={0.4} scale={10} blur={1.5} far={4.5} />
                    <OrbitControls enablePan enableZoom enableRotate />
                </Suspense>
            </Canvas>
        </div>
    );
};

Model.propTypes = {
    url: PropTypes.string.isRequired,
};

Listing3D.propTypes = {
    modelPath: PropTypes.string.isRequired,
};

export default Listing3D;
