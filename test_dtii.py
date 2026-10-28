from src.dtii.dtii_engine import DTIIEngine


engine = DTIIEngine()


features = {

    "seismic":
        7.5,

    "deformation":
        0.35,

    "elevation":
        20.0,

    "wave":
        2.2387,

    "inundation":
        58.9824,

    "prediction":
        0.3684,

}


print("\n" + "=" * 60)
print(" DTII TEST ")
print("=" * 60)


result = engine.compute(
    features
)


print("\nRAW FEATURES")

for key, value in features.items():

    print(
        f"{key:15} : {value}"
    )


print("\nNORMALIZED FEATURES")

for key, value in result[
    "features"
].items():

    print(
        f"{key:15} : {value:.4f}"
    )


print(
    "\nDTII SCORE :",
    result["score"]
)

print(
    "DTII LEVEL :",
    result["level"]
)

print("=" * 60)