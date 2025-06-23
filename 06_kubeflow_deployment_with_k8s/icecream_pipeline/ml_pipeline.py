from kfp import dsl
from kfp.components import create_component_from_func

from components.preprocess import preprocess
from components.train import train
from components.evaluate import evaluate


preprocess_op = create_component_from_func(preprocess, base_image="sklearn:v1")
train_op = create_component_from_func(train, base_image="sklearn:v1")
evaluate_op = create_component_from_func(evaluate, base_image="sklearn:v1")

@dsl.pipeline(
    name="Ice Cream Pipeline",
    description="Includes metrics, and volume sharing."
)
def ice_cream_pipeline(test_size: float = 0.2, random_state: int = 42):

    volume_op = dsl.VolumeOp(
        name="create-volume",
        resource_name="icecream-pvc",
        size="1Gi",
        modes=dsl.VOLUME_MODE_RWO
    )

    preprocess_step = preprocess_op(output_csv_path="/data/icecream_clean.csv")
    preprocess_step.add_pvolumes({"/data": volume_op.volume})

    train_step = train_op(
        input_csv_path="/data/icecream_clean.csv",
        model_path="/data/icecream_model.joblib"
    ).after(preprocess_step)
    train_step.add_pvolumes({"/data": preprocess_step.pvolume})

    evaluate_step = evaluate_op(
        model_path="/data/icecream_model.joblib",
        input_csv_path="/data/icecream_clean.csv"
    ).after(train_step)
    evaluate_step.add_pvolumes({"/data": train_step.pvolume})

# Compile pipeline
if __name__ == "__main__":
    from kfp.compiler import Compiler
    Compiler().compile(ice_cream_pipeline, "ice_cream_pipeline.yaml")
