meta_data_sampled.json是从MJHQ中随机采样出来的数据集，之后的实验统一使用这里的prompt生成，然后和数据集中的对应子集算FID和IR

/data2/hfc/feice-cloud/result
├── bf16: bf16的原模型结果
├── convrot_16: 大规模回退下，N0取16的结果
├── convrot_64: 大规模回退下，N0取64的结果
├── convrot_quality: 大规模回退下，N0取256的结果
├── convrot_standard: 小规模回退下，N0取256，type为standard的结果
├── convrot_random: 小规模回退下，N0取256，type为random的结果
├── convrot_regular: 小规模回退下，N0取256，type为regular的结果 <- 这个是我们方法的真实水平
├── lite: 无回退，无旋转的噪声结果
└── nunchaku: SVDQuant的结果

小规模回退的层: 
    "x_embedder",
    *[f"single_transformer_blocks.{i}.proj_out" for i in range(38)],
    "norm_out.linear",
    "proj_out",   