// External Libraries
import { useGLTF } from '@react-three/drei';
import PropTypes from 'prop-types';

const GLBModel = ({ modelPath }) => {
    const { scene } = useGLTF(modelPath);
    // eslint-disable-next-line react/no-unknown-property
    return <primitive object={ scene } />;
};

GLBModel.propTypes = {
    modelPath: PropTypes.string.isRequired,
};

export default GLBModel;
