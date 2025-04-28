// External Libraries
import { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { MTLLoader } from 'three/examples/jsm/loaders/MTLLoader';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader';
import PropTypes from 'prop-types';

const OBJModel = ({ modelPath }) => {
    const group = useRef();

    useEffect(() => {
        const manager = new THREE.LoadingManager();
        const pathParts = modelPath.split('/');
        const filename = pathParts.pop();
        const basePath = pathParts.join('/') + '/';
        const modelName = filename.split('.')[0];

        new MTLLoader(manager)
            .setPath(basePath)
            .load(`${ modelName }.mtl`, (materials) => {
                materials.preload();

                new OBJLoader(manager)
                    .setMaterials(materials)
                    .setPath(basePath)
                    .load(`${ modelName }.obj`, (object) => {
                        if (group.current) {
                            group.current.clear();
                            group.current.add(object);
                        }
                    });
            });
    }, [modelPath]);

    return <group ref={ group } />;
};

OBJModel.propTypes = {
    modelPath: PropTypes.string.isRequired,
};

export default OBJModel;
