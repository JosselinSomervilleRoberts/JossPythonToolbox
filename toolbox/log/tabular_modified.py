from dowel.tabular_input import TabularInput
import wandb

class TabularModified(TabularInput):

    def __init__(self, use_wandb=False, wandb_step_factor=1):
        super().__init__()
        self.use_wandb = use_wandb
        self.wandb_step_factor = wandb_step_factor

    def set_wandb(self, use_wandb, wandb_step_factor=1):
        self.use_wandb = use_wandb
        self.wandb_step_factor = wandb_step_factor

    def record(self, key, val, step=None):
        super().record(key, val)
        if self.use_wandb:
            prefix_str = '.'.join(self._prefixes) + "/" if len(self._prefixes) > 0 else ""
            if step is None:
                wandb.log({prefix_str + key: val})
            else:
                wandb.log({prefix_str + key: val}, step=step*self.wandb_step_factor)